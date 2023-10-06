import torch
import torch.nn as nn
import random
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from torchmetrics import MeanAbsolutePercentageError

random_seed = 222
torch.manual_seed(random_seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(random_seed)
torch.cuda.manual_seed(random_seed)
torch.cuda.manual_seed_all(random_seed) # multi-GPU

class Preprocessing:
    import pandas as pd

    def __init__(self, Input_type) -> None:
        self.Input_type = Input_type
        self.representative_weather = None

    def generate_target_df(self, weather_metadata_path, weather_5minute_ASOS_path, holiday_path, power_path):
        self.weather_metadata_path = weather_metadata_path
        self.weather_5minute_ASOS_path = weather_5minute_ASOS_path
        self.holiday_path = holiday_path
        self.power_path = power_path
        import pandas as pd

    # 기상관측 MetaData 불러오기
        self.weather_metadata = pd.read_csv(self.weather_metadata_path)
        self.STN_dict = {STN_name : STN_num for STN_num, STN_name in zip(self.weather_metadata['지점'], self.weather_metadata['지점명'])}
        self.target_STN_list = [self.STN_dict[STN_name] for STN_name in ['서울', '부산', '인천', '대구', '대전', '광주', '원주']]

        # 서울 포함 7개 도시의 기온 및 일사량 데이터 불러오기
        self.weather_5minute = pd.read_parquet(self.weather_5minute_ASOS_path).astype({'지점' : 'int'})
        self.weather_5minute = self.weather_5minute[self.weather_5minute['지점'].isin(self.target_STN_list)]
        self.weather_5minute = self.weather_5minute[['지점', '일시', '기온(°C)', '일사(MJ/m^2)']]
        self.weather_5minute.columns = ['지점', '일시', '기온', '일사']

        self.column_list = ['기온', '일사']

    # 선형보간법 사용하여 결측값 채우기
        for idx, STN in enumerate(self.target_STN_list):

            # ① 각 STN별로 데이터 나누기
            self.tmp = self.weather_5minute[self.weather_5minute['지점'] == STN]

            # ② 시간순으로 정렬하기
            self.tmp = self.tmp.sort_values(by='일시')

            # ③ 선형보간법을 사용하여 nan값 채우기                
            for column in self.column_list:
                self.tmp[column] = self.tmp[column].interpolate(method='linear')

            # ④ tmp 합치기
            if idx == 0:
                self.interpolated_weather = self.tmp
            else:
                self.interpolated_weather = pd.concat([self.interpolated_weather, self.tmp])

    # 전국 기상 대표값 정하기 (최고기온, 최저기온, 평균일사량)
        for idx, column in enumerate(self.column_list):
            if column == '기온':
                # 최고 기온
                self.tmp_1 = pd.DataFrame(self.interpolated_weather.groupby('일시', as_index = False)[column].max()).rename(columns = {'기온' : 'max_temp'})
                # 최저 기온
                self.tmp_2 = pd.DataFrame(self.interpolated_weather.groupby('일시', as_index = False)[column].min()).rename(columns = {'기온' : 'min_temp'})
                self.tmp = pd.merge(self.tmp_1, self.tmp_2, on = '일시', how = 'inner')
            else:
            # 평균 일사량
                self.tmp = pd.DataFrame(self.interpolated_weather.groupby('일시', as_index = False)[column].mean()).rename(columns = {'일사' : 'mean_insolation'})
            # ② groupby 결과를 인덱스 기준으로 Join
            if idx == 0:
                self.representative_weather = self.tmp
            else:
                self.representative_weather = pd.merge(self.representative_weather, self.tmp, on = '일시', how = 'inner')

        self.representative_weather.rename(columns = {'일시' : 'datetime'}, inplace= True)

        # 요일 특성 반영 (더미변수로 반영)
        # 0 : 월요일, 1 : 화요일 ~ 금요일, 2 : 토요일, 3 : 일요일

        self.representative_weather['weekday'] = pd.to_datetime(self.representative_weather['datetime']).dt.weekday
        self.representative_weather.replace({'weekday' : {2 : 1, 3 : 1, 4 : 1, 5 : 2, 6 : 3}}, inplace = True)
        self.representative_weather = pd.get_dummies(self.representative_weather, columns = ['weekday'])
                                            
        # 휴일 유형에 맞춘 더미변수 반영

        self.holiday = pd.read_csv(self.holiday_path)

        for dateName in ['국회의원선거일', '대통령선거일', '동시지방선거일', '전국동시지방선거', '제21대 국회의원선거']:
            self.holiday.replace({'dateName' : {dateName : '선거일'}}, inplace = True)

        self.holiday.replace({'dateName' : {'1월1일' : '신정'}}, inplace = True)
        self.holiday.replace({'dateName' : {'부처님오신날' : '석가탄신일'}}, inplace = True)
        self.holiday.replace({'dateName' : {'어린이 날' : '어린이날'}}, inplace = True)
        self.holiday.replace({'dateName' : {'대체휴무일' : '대체공휴일'}}, inplace = True)
        self.holiday.replace({'dateName' : {'임시공휴일' : '대체공휴일'}}, inplace = True)

        self.nameToNumber = {dateName : idx + 1  for idx, dateName in enumerate(list(self.holiday['dateName'].unique()))}
        self.holiday.replace({'dateName' : self.nameToNumber}, inplace = True)
        self.holiday_dict = {locdate : dateName for dateName, locdate in zip(self.holiday['dateName'], self.holiday['locdate'])}

        for row_number in range(self.representative_weather.shape[0]):
            if self.representative_weather.at[row_number, 'datetime'][:-6] in list(self.holiday['locdate']):
                self.representative_weather.at[row_number, 'holiday'] = self.holiday_dict[self.representative_weather.at[row_number, 'datetime'][:-6]]
            else:
                self.representative_weather.at[row_number, 'holiday'] = 0

        self.representative_weather = pd.get_dummies(self.representative_weather, columns = ['holiday'])

        # 월, 시간 정보 반영 (더미변수로 반영)

        self.representative_weather['month'] = pd.to_datetime(self.representative_weather['datetime']).dt.month
        self.representative_weather = pd.get_dummies(self.representative_weather, columns = ['month'])
        self.representative_weather['hour'] = pd.to_datetime(self.representative_weather['datetime']).dt.hour
        self.representative_weather = pd.get_dummies(self.representative_weather, columns = ['hour'])

        

        self.power = pd.read_parquet(self.power_path)
        self.power['load'] = self.power['demand']
        self.power.drop(columns='demand', inplace = True)
        self.power.reset_index(inplace = True)
        self.power = self.power.astype({'datetime' : 'str'})
        for row_number in range(self.power.shape[0]):
            self.power.loc[row_number, 'datetime'] = self.power.loc[row_number, 'datetime'][:-3]

    # 기상정보, 달력정보, 전력정보를 하나의 데이터 프레임으로 합치기

        self.target_df = pd.merge(self.representative_weather, self.power, on = 'datetime', how = 'inner')[:-288]
        self.target_df = pd.concat([self.target_df.iloc[:, :4], self.target_df.iloc[:, -12:-1], self.target_df.iloc[:, 4:-12], self.target_df.iloc[:, -1]], axis = 1)


        if self.Input_type == 'Type_1':
            return self.target_df[['datetime', 'load']]
        
        elif self.Input_type == 'Type_2':
            return self.target_df[['datetime', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
                                    'holiday_0.0', 'holiday_1.0', 'holiday_2.0', 'holiday_3.0',
                                    'holiday_4.0', 'holiday_5.0', 'holiday_6.0', 'holiday_7.0',
                                    'holiday_8.0', 'holiday_9.0', 'holiday_10.0', 'holiday_11.0',
                                    'holiday_12.0', 'holiday_13.0', 'month_1', 'month_2', 'month_3',
                                    'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
                                    'month_10', 'month_11', 'month_12', 'hour_0', 'hour_1', 'hour_2',
                                    'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                                    'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15',
                                    'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21',
                                    'hour_22', 'hour_23', 'load']]

        elif self.Input_type == 'Type_3':
            return self.target_df[['datetime', 'shift_1day', 'shift_1week', '24hour_High', '24hour_Low',
                                    'moving_avg_30min', 'moving_avg_6hour', 'moving_avg_1day',
                                    'moving_avg_1week', 'moving_avg_4week', 'moving_avg_12week',
                                    'moving_avg_6mon', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
                                    'holiday_0.0', 'holiday_1.0', 'holiday_2.0', 'holiday_3.0',
                                    'holiday_4.0', 'holiday_5.0', 'holiday_6.0', 'holiday_7.0',
                                    'holiday_8.0', 'holiday_9.0', 'holiday_10.0', 'holiday_11.0',
                                    'holiday_12.0', 'holiday_13.0', 'month_1', 'month_2', 'month_3',
                                    'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
                                    'month_10', 'month_11', 'month_12', 'hour_0', 'hour_1', 'hour_2',
                                    'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                                    'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15',
                                    'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21',
                                    'hour_22', 'hour_23', 'load']]
            
        elif self.Input_type == 'Type_4':
            return self.target_df[['datetime', 'min_temp', 'max_temp', 'mean_insolation', 
                                    'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
                                    'holiday_0.0', 'holiday_1.0', 'holiday_2.0', 'holiday_3.0',
                                    'holiday_4.0', 'holiday_5.0', 'holiday_6.0', 'holiday_7.0',
                                    'holiday_8.0', 'holiday_9.0', 'holiday_10.0', 'holiday_11.0',
                                    'holiday_12.0', 'holiday_13.0', 'month_1', 'month_2', 'month_3',
                                    'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
                                    'month_10', 'month_11', 'month_12', 'hour_0', 'hour_1', 'hour_2',
                                    'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                                    'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15',
                                    'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21',
                                    'hour_22', 'hour_23', 'load']] 
            
        elif self.Input_type == 'Type_5':
            return self.target_df
        
    def split(self, df):
        self.df = df
        if self.Input_type == 'Type_1':
            return self.df.iloc[:-8064], self.df.iloc[-8064:-2016], self.df.iloc[-4032:]
        else:
            return self.df.iloc[:-8064,:], self.df.iloc[-8064:-2016,:], self.df.iloc[-4032:,:]
        
    def get_device(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        return self.device


# Train 데이터셋을 위한 Custom Dataset은 Scaler의 fit_transform 기능을 이용
# Type_1의 경우 except 구문 실행

class CustomDatasetForTrain(torch.utils.data.Dataset):
    def __init__(self, target_df, binary_var_start_number, scaler_for_X, scaler_for_Y, seq_len, step_len, stride, device):
        try:
            self.dataset_tensor = torch.FloatTensor(np.array(pd.concat([pd.DataFrame(scaler_for_X.fit_transform(target_df.iloc[:,1:-1])),\
                                                                pd.DataFrame(scaler_for_Y.fit_transform(np.array(target_df['load']).reshape(-1, 1)))], axis = 1))).to(device)
        except:
            self.dataset_tensor = torch.FloatTensor(np.array(pd.DataFrame(scaler_for_Y.fit_transform(np.array(target_df['load']).reshape(-1, 1))))).to(device)
        self.data_size = ((self.dataset_tensor.shape[0] - step_len - seq_len) // stride) + 1
        self.seq_len = seq_len
        self.step_len = step_len
        self.stride= stride
    
    def __len__(self):
        return self.data_size
    
    def __getitem__(self, idx):
        return self.dataset_tensor[idx*self.stride :idx*self.stride + self.seq_len, :],\
            self.dataset_tensor[idx*self.stride + self.seq_len : idx*self.stride + self.seq_len + self.step_len, -1]

# Test 데이터셋을 위한 Custom Dataset은 Scaler의 Transform 기능을 이용

class CustomDatasetForValTest(torch.utils.data.Dataset):
    def __init__(self, target_df, binary_var_start_number, scaler_for_X, scaler_for_Y, seq_len, step_len, stride, device):
        try:
            self.dataset_tensor =torch.FloatTensor(np.array(pd.concat([pd.DataFrame(scaler_for_X.transform(target_df.iloc[:,1:-1])),\
                                                                    pd.DataFrame(scaler_for_Y.transform(np.array(target_df['load']).reshape(-1, 1)))], axis = 1))).to(device)
        except:
            self.dataset_tensor = torch.FloatTensor(np.array(pd.DataFrame(scaler_for_Y.transform(np.array(target_df['load']).reshape(-1, 1))))).to(device)                     
        self.data_size = ((self.dataset_tensor.shape[0] - step_len - seq_len) // stride)+1
        self.seq_len = seq_len
        self.step_len = step_len
        self.stride= stride
    
    def __len__(self):
        return self.data_size
    
    def __getitem__(self, idx):
        return self.dataset_tensor[idx*self.stride :idx*self.stride + self.seq_len, :],\
            self.dataset_tensor[idx*self.stride + self.seq_len : idx*self.stride + self.seq_len + self.step_len, -1]
        
def model_load(Input_type, Model, path):
    path = path
    file_name = Input_type + '_' + Model + '.pth'
    out = path + file_name
    return torch.load(out, map_location='cpu')
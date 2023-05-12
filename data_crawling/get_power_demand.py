# start_date, end_date는 str 형식으로 입력해야하며, 반환값은 DataFrame임

def get_power_demand(start_date, end_date):
    
    if not isinstance(start_date, str):
        return print('Check start_date')
    elif not isinstance(end_date, str):
        return print('Check end_date')

    import pandas as pd
    import datetime
    import time

    url = f"http://www.happydr.co.kr/?act=&mid=CurrentSupplyView&vid=&view=table&option_date={start_date}"
    start_date = datetime.datetime.strptime(start_date, '%Y%m%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d').date()
    tmp_date = start_date

    col_order = pd.read_html(url)[1].columns.tolist()
    df = pd.DataFrame()

    while True:
        url = f"http://www.happydr.co.kr/?act=&mid=CurrentSupplyView&vid=&view=table&option_date={start_date}"
        data = pd.read_html(url)[2]
        data = data[::-1]

        df = pd.concat([df, data], axis=0)
        
        time.sleep(0.2)

        start_date += datetime.timedelta(1)

        if start_date > end_date:
            break

    df.sort_values(by=0, inplace=True)
    df.columns = col_order
    df.reset_index(drop=True, inplace=True)
    print(f'Complete {tmp_date} to {end_date}')

    return df

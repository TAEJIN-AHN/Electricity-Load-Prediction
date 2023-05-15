#  1. TM     : 관측시각 (KST)
#  2. STN    : 국내 지점번호
#  3. WD     : 풍향 (16방위)
#  4. WS     : 풍속 (m/s)
#  5. GST_WD : 돌풍향 (16방위)
#  6. GST_WS : 돌풍속 (m/s)
#  7. GST_TM : 돌풍속이 관측된 시각 (시분)
#  8. PA     : 현지기압 (hPa)
#  9. PS     : 해면기압 (hPa)
# 10. PT     : 기압변화경향 (Code 0200) 
# 11. PR     : 기압변화량 (hPa)
# 12. TA     : 기온 (C)
# 13. TD     : 이슬점온도 (C)
# 14. HM     : 상대습도 (%)
# 15. PV     : 수증기압 (hPa)
# 16. RN     : 강수량 (mm) : 여름철에는 1시간강수량, 겨울철에는 3시간강수량
# 17. RN_DAY : 일강수량 (mm) : 해당시간까지 관측된 양(통계표)
# 18. RN_JUN : 일강수량 (mm) : 해당시간까지 관측된 양을 전문으로 입력한 값(전문)
# 19. RN_INT : 강수강도 (mm/h) : 관측하는 곳이 별로 없음
# 20. SD_HR3 : 3시간 신적설 (cm) : 3시간 동안 내린 신적설의 높이
# 21. SD_DAY : 일 신적설 (cm) : 00시00분부터 위 관측시간까지 내린 신적설의 높이
# 22. SD_TOT : 적설 (cm) : 치우지 않고 그냥 계속 쌓이도록 놔눈 경우의 적설의 높이
# 23. WC     : GTS 현재일기 (Code 4677)
# 24. WP     : GTS 과거일기 (Code 4561) .. 3(황사),4(안개),5(가랑비),6(비),7(눈),8(소나기),9(뇌전)
# 25. WW     : 국내식 일기코드 (문자열 22개) : 2자리씩 11개까지 기록 가능 (코드는 기상자원과 문의)
# 26. CA_TOT : 전운량 (1/10)
# 27. CA_MID : 중하층운량 (1/10)
# 28. CH_MIN : 최저운고 (100m)
# 29. CT     : 운형 (문자열 8개) : 2자리 코드로 4개까지 기록 가능
# 30. CT_TOP : GTS 상층운형 (Code 0509)
# 31. CT_MID : GTS 중층운형 (Code 0515)
# 32. CT_LOW : GTS 하층운형 (Code 0513)
# 33. VS     : 시정 (10m)
# 34. SS     : 일조 (hr)
# 35. SI     : 일사 (MJ/m2)
# 36. ST_GD  : 지면상태 코드 (코드는 기상자원과 문의)
# 37. TS     : 지면온도 (C)
# 38. TE_005 : 5cm 지중온도 (C)
# 39. TE_01  : 10cm 지중온도 (C)
# 40. TE_02  : 20cm 지중온도 (C)
# 41. TE_03  : 30cm 지중온도 (C)
# 42. ST_SEA : 해면상태 코드 (코드는 기상자원과 문의)
# 43. WH     : 파고 (m) : 해안관측소에서 목측한 값
# 44. BF     : Beaufart 최대풍력(GTS코드)
# 45. IR     : 강수자료 유무 (Code 1819) .. 1(Sec1에 포함), 2(Sec3에 포함), 3(무강수), 4(결측)
# 46. IX     : 유인관측/무인관측 및 일기 포함여부 (code 1860) .. 1,2,3(유인) 4,5,6(무인) / 1,4(포함), 2,5(생략), 3,6(결측)

def get_weather_fromland(start_date,end_date,auth) -> pd.DataFrame:
    import datetime
    
    #날짜 정의
    start_date = str(start_date)
    end_date = str(end_date)
    start_date = datetime.datetime.strptime(start_date,"%Y%m%d").date()
    end_date = datetime.datetime.strptime(end_date,"%Y%m%d").date()
    days = (end_date - start_date).days + 1

    #API 정의
    base = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php?'
    authKey=f'authKey={auth}'
    
    # 빈 df 정의
    df =  pd.DataFrame()
    
    # API 호출
    if days > 29:
        batch = days // 29 + 1
    else:
        batch = 1
    for i in range(batch):
        
        if start_date - datetime.timedelta(1) == end_date:
            break
        elif i+1 == batch:
            to_date = start_date + datetime.timedelta(days % 29)
        else:
            to_date = start_date + datetime.timedelta(29)
            
        # 날짜 텍스트화
        str_from_date = start_date.strftime('%Y%m%d')
        str_to_date = to_date.strftime('%Y%m%d')
        # url 정의
        url = base + f'tm1={str_from_date}0000&' + f'tm2={str_to_date}2300&' + 'help=0&' + authKey
        print(f'current_batch : {i + 1}/{batch}, current_date : {str_from_date} - {str_to_date}')
        # 데이터 생성
        try:
            print(url)
            df_tmp = get_parse_weather(url)
        except:
            print(f'error occured on {str_to_date}')
            df = pd.concat([df,df_tmp])
            break
        
        df = pd.concat([df,df_tmp])
        # 시작일 재정의
        start_date = to_date + datetime.timedelta(1)
        print(days)

    # 날짜 형식 변환
    df['datetime'] = pd.to_datetime(df['YYMMDDHHMI_KST'], format='%Y%m%d%H%M')
    df['datetime'] = df['datetime'].apply(lambda x : x.strftime(format='%Y-%m-%d %H:%M'))
    
    # 컬럼 순서 정리
    df.drop(['YYMMDDHHMI_KST'],axis=1,inplace=True)
    cols = df.columns.tolist()
    cols = [cols[-1]] + [col for col in cols[:-1]]
    df = df[cols]

    return df

def get_parse_weather(url):
    df =  pd.DataFrame()
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    col_1d = soup.text.split('\n')[2]
    col_2d = soup.text.split('\n')[3]
    data = soup.text.split('\n')[4:-2]

    # 행 정리
    df = pd.DataFrame(data, columns=['data'])
    df = pd.concat([df['data'].str.split(expand=True)], axis=1)
    
    # 컬럼 정리
    col_1d = col_1d.split()[1:]
    col_2d = col_2d.split()[1:]

    col_2d.insert(col_2d.index('LOW'),'-')
    col_2d.insert(col_2d.index('LOW'),'-')
    col_2d.insert(col_2d.index('LOW'),'-')
    col_2d = ['nan' if x.startswith('-') else x for x in col_2d]

    cols = [col_1d[i] + '_' + col_2d[i] for i in range(len(col_1d))]
    df.columns = cols
    return df

auth = 본인 키!
df = get_weather_fromland(20130101,20230512,auth)
df.to_csv('./weather_fromland_20190101_20230319.csv')

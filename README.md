# 세상에서 가장 가벼운 단기 전력수요 예측 모델
## **요약**
### **① 기본 정보**
* 팀구성 및 기여도 : 5명 / 20%
* 담당 역할
  * Pytorch를 이용한 CNN + LSTM(or GRU) 신경망 모델 구축
  * 기상 정보와 전력 수요에 대한 EDA, 데이터 전처리 및 시각화

### **② 프로젝트 진행 배경**
* 통상적으로 전력 수요 예측에는 기온, 일사량 등을 포함한 기상정보가 활용되고 있습니다.
* 그러나 전력 수요 데이터는 매우 일정한 패턴을 가지고 있다는 점에서 아래와 같은 의문이 생겼습니다.
<p align = 'center'><i>기상정보 없이 전력 수요 예측이 가능하다면?</i></p>

* 아래와 사항을 검증하여 과거의 패턴만으로 전력 수요 예측이 가능하다는 가설을 증명하고자 합니다.
<p align = 'center'><i>기상 정보를 활용한 예측 모델과 아닌 모델의 MAPE 차이는 1%p 이내 일 것이다.</i></p>

### **③ 결과 및 직무에 적용할 점**
* 변수 조합에 따라 CNN + LSTM 모델을 구축, 성능을 비교한 결과 제기한 가설이 참임을 증명하였습니다.

  * LSTM, GRU 등 RNN 기반 알고리즘을 활용한 상품 및 서비스 수요 예측을 수행할 수 있습니다.
  * Pytorch 등의 ML/DL 프레임워크를 활용하기 위한 시계열 데이터 전처리 업무를 할 수 있습니다.

### **④ 주요 액션**
<p align = 'center'><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/6b68e8b5-2127-4ca3-aa39-6a864d35325d' width = 70%></p>

## **상세**

### **① 데이터 수집**
* 자세한 내용과 코드는 [링크](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/main/EDA_MAIN.ipynb)를 참고해주시기 바랍니다.
* 프로젝트 진행에 앞서 웹 크롤링 및 OpenAPI 등을 활용해 아래와 같은 데이터를 수집함
  
  <table align = 'center'>
	  <tr>
		  <th align = 'center'>수집 대상</th>
		  <th align = 'center'>수집 방법</th>
		  <th align = 'center'>수집 출처</th>
	  </tr>
	  <tr>
		  <td align = 'center'>5분 간격 기상정보</td>
		  <td align = 'center'>웹 크롤링</td>
		  <td align = 'center'><a href = 'https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36&tabNo=1'>기상청 기상자료개방포털</a></td>
	  </tr>
	  <tr>
		  <td align = 'center'>5분 간격 전력 수요</td>
		  <td align = 'center'>Open API</td>
		  <td align = 'center'><a href = 'https://www.gridwiz.com/kr/'>그리드 위즈</a></td>
	  </tr>
	  <tr>
		  <td align = 'center'>달력(공휴일) 정보</td>
		  <td align = 'center'>Open API</td>
		  <td align = 'center'><a href = 'https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690'>한국천문연구원 특일 정보</a></td>
	  </tr>
  </table>

### **② 데이터 전처리**
* 자세한 내용과 코드는 [링크](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/main/EDA_MAIN.ipynb)를 참고해주시기 바랍니다.
* **5분 간격 전력 수요 정보 보간 (Interpolation)**
  
  * 본 프로젝트에서 수집한 5분 간격 전력수요 데이터는 결측치의 비중이 높음
  * 여러 보간법 중 최적의 방법을 선택하기 위해 아래와 같은 순서로 실험을 진행함

    <p align = 'center'><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/d00a3dc1-4644-4983-9021-ae3cb52d7c9c'></p>

#### B.3. 데이터셋 소개 및 인사이트
**전력수요 EDA 결과**
- 전력 수요는 명확한 계절성을 가지며, 연도에 관계없이 시간대별 패턴이 일관되게 유지됩니다.
- 전력 수요에는 폭염이나 코로나와 같은 외부 요인이 반영되며, 계절성 패턴이 안정적으로 유지됩니다.
- 전력 수요는 주로 산업 수요에 의해 영향을 받습니다.
- ACF 분석 결과, 전력 수요는 과거의 패턴에 기반한 자기회귀성을 가진 시계열 데이터임을 확인했습니다.
- 

**기상정보 EDA 결과**
- 전력 수요와 기상정보 간에는 상관관계가 있지만, 상당한 노이즈가 존재합니다.
- 특히 온도와 일사량은 전력 수요와 상관관계가 있으며, 온도의 양극단에서는 더 높은 상관관계를 보입니다.
- 그러나 기상요인 중 전력 수요와 높은 상관관계를 가지고 있는 일사량 데이터의 결측이 많이 발생하고 있습니다.
![](https://i.imgur.com/ZW7RQ8L.png)

**WRAP UP**
- 기상 요소는 전력 수요에 일부 영향을 미칩니다.
- 전력 수요 데이터에는 이미 과거의 사회/계절적 요인이 반영되어 있습니다.
- 달력 데이터와 보조 지표의 조합은 성능 개선이 미미합니다.
- 성능이 유사한 경우, 경제성 원칙에 따라 달력 데이터와 전력 수요 데이터만을 사용하는 모델이 적합할 것입니다.

#### B.4. 결과
![](https://i.imgur.com/zi2NPT4.png)
- <fig 6>

![](https://i.imgur.com/Uy6Q4b9.png)
- <fig 3>

![](https://i.imgur.com/08piGPK.png)
- <fig 4>

**실험 결과 차트**

| 파라미터                  | Type 1    | Type 2         | Type 3                       | Type 4              | Type 5                            |
| ------------------------- | --------- | -------------- | ---------------------------- | ------------------- | --------------------------------- |
| features                      | 전력 수요 | 전력 수요,달력 | 전력 수요,달력,전력 보조지표 | 전력 수요,달력,날씨 | 전력 수요,달력,날씨,전력 보조지표 |
| in_dim                    | 1         | 55             | 66                           | 58                  | 69                                |
| CNN-out_dim               | in * 2    | in * 2         | in * 2                       | in * 2              | in * 2                            |
| CNN-kernel | 5         | 5              | 5                            | 5                   | 5                                 |
| hidden_dim          | 288       | 288            | 288                          | 288                 | 288                               |
| Layer                     | 3         | 3              | 3                            | 3                   | 3                                 |
| Learning Rate             | 0.0001    | 0.0001         | 0.0001                       | 0.0001              | 0.0001                            |
| Epochs                    | 50        | 50             | 50                           | 50                  | 50                                |
| MAPE - CNN-LSTM(bi)       | 13.09%    | 3.29%          | 3.26%                        | 3.50%               | 2.88%                             |
| MAPE - CNN-GRU(bi)        | 8.75%     | 3.38%          | 3.48%                        | 3.80%               | 4.78%                             |

**실험 분석**
- Type 1을 제외한 모든 모델의 성능이 한국전력거래소(KPX) 대비 7% 이상 우수하게 나타났습니다. (fig. 6)
    - 따라서 전력 데이터와 달력 데이터만 사용하여 기존 모델을 대체할 수 있습니다.
- Type 2와 Type 4의 성능은 각각 3.29%와 3.50%로, Type 2의 성능이 Type 4에 비해 약 6% 우수합니다. (fig. 3)
    - 따라서 날씨 데이터의 추가는 성능 저하로 이어집니다.
- Type 2와 Type 3의 성능은 각각 3.29%와 3.26%로, Type 2와 Type 3의 성능은 유사합니다. (fig. 4)
    - 따라서 달력 데이터와 보조 지표의 조합은 성능 개선이 미미합니다.
    - 성능이 유사한 경우, 경제성 원리에 따라 Type 2 모델이 적합합니다.
*(KPX = 한국전력거래소의 예측치)*

**결론 도출**
1. Type 2의 입력인 전력 수요 데이터와 달력 데이터만 사용하여도 기상정보를 사용하는 것과 동일한 성능을 얻을 수 있음을 검증하였습니다.
2. 따라서 '과거의 패턴만으로도 미래의 전력 수요를 예측할 수 있다'는 가설이 참임을 입증하였습니다.

### C. Deck
---
프로젝트를 정리한 PPT 자료입니다.<br>
[세상에서 가장 가벼운 전력 수요 예측](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/fec7867dec8ffc3f2a7e55be883e242a3cc61513/presentation/model_presentation.pdf)

### D. Methods Used
---
- 딥러닝 라이브러리
	- torch Version : 2.0.1+cu118
	- torchmetrics Version : 0.11.4
- 모델
	- CNN-LSTM
	- CNN-GRU
- 시각화
	- matplotlib
	- seaborn
- 데이터 전처리
	- sklearn Version : 1.2.2
	- pandas Version : 1.5.3 
	- numpy Version : 1.24.3
- 개발 환경
	- Colab
	- Python 3.9

### E. Contributing Members
---
| Name   | github                                             |
| ------ | -------------------------------------------------- |
| 나인성 | [InSung-Na · GitHub](https://github.com/inSung-Na) |
| 남영   | [skadudd · GitHub](https://github.com/skadudd)     |
| 박지호 |   [jihosuperman · GitHub](https://github.com/jihosuperman)                                                 |
| 안태진       | [TAEJIN-AHN · GitHub](https://github.com/TAEJIN-AHN)                                                   |
| 황승주 | [peracer · GitHub](https://github.com/peracer)     |

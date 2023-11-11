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

  * 결측 구간이 짧을 때는 선형 보간법이 우세하나, 길어질 수록 Median을 사용한 보간이 우세함
    <p align = 'center'><img src = https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/9f40ec43-4b72-45a3-beb5-5b05191d5b1f' width = 80%></p>

  * 실험 결과를 통해 아래와 같은 보간 규칙을 적용하기로 결정함
    * 연속 20일 이상의 결측 구간 : 주변일 전력수요의 중앙값으로 보간
    * 연속 20일 이하의 결측 구간 : 선형 보간법 활용

* **그 외 전처리**
  * 5분 간격 기상정보 : 선형 보간법 활용하여 결측값 보완
  * 달력(공휴일) 정보 : 휴일 유형에 맞춘 더미 변수를 모델 학습에 활용하기 위해 휴일 이름을 통일
    <p>예) 부처님오신날 → 석가탄신일, 임시공휴일, 대체휴무일 → 대체공휴일</p>

### **③ EDA**
* 자세한 내용과 코드는 [링크](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/main/EDA_MAIN.ipynb)를 참고해주시기 바랍니다.
* EDA를 통해 확인한 주요 내용은 다음과 같음
  * **전력 수요는 자기 회귀성을 가진 시계열 데이터임**
    
    * 같은 요일, 같은 시간의 자기 상관은 높은 수치를 보임
    * 연간 자기상관은 3개월을 기준으로 상승과 하강을 반복함
      <p><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/f08a5528-6ecc-4d34-808a-214fd872e1f8'></p>
    * 모델 학습 시, 이동평균 등의 기술지표와 요일, 시간대 등의 시간 정보를 반드시 포함하도록 함
  * **기상정보 중 기온과 일사량이 전력 수요와 상대적으로 높은 상관관계를 가짐**

    <p><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/b414f9be-160f-4aaf-a3a9-9920d730f5dc'></p>

* 그 외 EDA를 통해 발견한 사항은 다음과 같음
  * 코로나19가 유행한 2019- 20년, 산업 전력 수요가 줄어들며 전국 전력 수요가 일시적으로 하락함
  * 월별 태양광 전력거래량은 계속해서 증가하는 추세에 있으며, 대부분 봄에 가장 높은 수치를 기록함
    <p>단, 태양광 발전량은 실시간으로 계량되지 않고, 추정 또한 어려워 모델 학습에는 사용하지 않음</p>

### **④ 모델링**
* 자세한 내용과 코드는 [링크](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/main/Model_MAIN.ipynb)를 참고해주시기 바랍니다.
* 아래와 같은 데이터를 기반으로 Sequential Dataset을 구성함
  
  <table align = 'center'>
	  <tr>
		  <th align = 'center'>분류</th>
		  <th align = 'center'>내용</th>
	  </tr>
	  <tr>
		  <td align = 'center'>ⓐ 전력 수요</td>
		  <td align = 'center'>5분 간격 전국 전력 수요</td>
	  </tr>
	  <tr>
		  <td rowspan = '4' align = 'center'>ⓑ 달력 및 시간 정보</td>
		  <td align = 'center'>요일 (더미변수)</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '4' align = 'center'>ⓑ 달력 및 시간 정보</td>-->
		  <td align = 'center'>휴일 (더미변수)</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '4' align = 'center'>ⓑ 달력 및 시간 정보</td>-->
		  <td align = 'center'>월(1~12, 더미변수)</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '4' align = 'center'>ⓑ 달력 및 시간 정보</td>-->
		  <td align = 'center'>시간대(0~23, 더미변수)</td>
	  </tr>
	  <tr>
		  <td rowspan = '3' align = 'center'>ⓒ 기상 대표값※</td>
		  <td align = 'center'>전국 최고 기온</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '3' align = 'center'>ⓒ 기상 대표값※</td>-->
		  <td align = 'center'>전국 최저 기온</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '3' align = 'center'>ⓒ 기상 대표값※</td>-->
		  <td align = 'center'>평균 일사량</td>
	  </tr>
	  <tr>
		  <td rowspan = '2' align = 'center'>ⓓ 보조 지표</td>
		  <td align = 'center'>1일 및 1주 전 동시간대 전력수요</td>
	  </tr>
	  <tr>
		  <!--<td rowspan = '2' align = 'center'>ⓓ 보조 지표</td>-->
		  <td align = 'center'>그 외 3개</td>
	  </tr>
  </table>
  <p align = 'center'>※ 기상 데이터의 결측치의 비중이 낮은 전국 특별시 및 광역시의 기온 및 일사량을 바탕으로 선정</p>
  <p align = 'center'><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/6c7290e5-73ff-4816-bba9-cd3e9dd05bfe' width = 80%></p>

* Feature의 조합을 기준으로 비교군/대조군을 설정하여 CNN+LSTM(GRU) 모델을 학습, 성능을 비교함
  
  * Type 2와 Type 4의 MAPE는 3.29%, 3.5%로 기상정보를 제외한 모델의 성능이 상대적으로 우수함
    
    <table align = 'center'>
     <tr>
        <th align = 'center' style = 'padding : 3px'>변수 조합(기호)</th>
        <th align = 'center' style = 'padding : 3px'>ⓐ</th>
        <th align = 'center' style = 'padding : 3px'>ⓐ, ⓑ</th>
        <th align = 'center' style = 'padding : 3px'>ⓐ, ⓑ, ⓓ</th>
        <th align = 'center' style = 'padding : 3px'>ⓐ, ⓑ, ⓒ</th>
        <th align = 'center' style = 'padding : 3px'>ⓐ, ⓑ, ⓒ, ⓓ</th>
    </tr>
    <tr>
        <td align = 'center' style = 'padding : 3px'>MAPE(CNN+LSTM)</td>
        <td align = 'center' style = 'padding : 3px'>13.09%</td>
        <td align = 'center' style = 'padding : 3px'><span style = 'color : red'><b>3.29%</b></span></td>
        <td align = 'center' style = 'padding : 3px'>3.26%</td>
        <td align = 'center' style = 'padding : 3px'><span style = 'color : red'><b>3.50%</b></span></td>
        <td align = 'center' style = 'padding : 3px'>2.88%</td>
    </tr>
        <tr>
        <td align = 'center' style = 'padding : 3px'>MAPE(CNN+GRU)</td>
        <td align = 'center' style = 'padding : 3px'>8.75%</td>
        <td align = 'center' style = 'padding : 3px'>3.38%</td>
        <td align = 'center' style = 'padding : 3px'>3.48%</td>
        <td align = 'center' style = 'padding : 3px'>3.80%</td>
        <td align = 'center' style = 'padding : 3px'>4.78%</td>
    </tr>
</table>

### **⑤ 결과 및 기대효과**

* 위의 결과를 통해 본 프로젝트에서 검증하고자 했던 아래의 가설이 참임을 입증함
<p align = 'center'><i>기상 정보를 활용한 예측 모델과 아닌 모델의 MAPE 차이는 1%p 이내 일 것이다.</i></p>
* 기상 정보를 제외함으로써 데이터 처리 비용을 줄이고 전력 수요 예측의 경제성을 높일 것으로 기대됨
<p align = 'center'><img src = 'https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/6863c30d-f7bd-433a-9339-74410f439434' width = 80%></p>

## Contributing Members
<table align = 'center'>
	<tr>
		<th align = 'center'>Name</th>
		<th align = 'center'>GitHub</th>
	</tr>
	<tr>
		<td align = 'center'>나인성</td>
		<td align = 'center'><a href = 'https://github.com/inSung-Na'>InSung-Na · GitHub</a></td>
	</tr>
	<tr>
		<td align = 'center'>남영</td>
		<td align = 'center'><a href = 'https://github.com/skadudd'>skadudd · GitHub</a></td>
	</tr>
	<tr>
		<td align = 'center'>박지호</td>
		<td align = 'center'><a href = 'https://github.com/jihosuperman'>jihosuperman · GitHub</a></td>
	</tr>
	<tr>
		<td align = 'center'>안태진</td>
		<td align = 'center'><a href = 'https://github.com/TAEJIN-AHN'>TAEJIN-AHN · GitHub</a></td>
	</tr>
	<tr>
		<td align = 'center'>황승주</td>
		<td align = 'center'><a href = 'https://github.com/peracer'>peracer · GitHub</a></td>
	</tr>
</table>


| Name   | github                                             |
| ------ | -------------------------------------------------- |
| 나인성 | [InSung-Na · GitHub](https://github.com/inSung-Na) |
| 남영   | [skadudd · GitHub](https://github.com/skadudd)     |
| 박지호 |   [jihosuperman · GitHub](https://github.com/jihosuperman)                                                 |
| 안태진       | [TAEJIN-AHN · GitHub](https://github.com/TAEJIN-AHN)                                                   |
| 황승주 | [peracer · GitHub](https://github.com/peracer)     |

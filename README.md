# 세상에서 가장 가벼운 전력 예측 모델
### A. TOC
- [세상에서 가장 가벼운 전력 예측 모델](#세상에서-가장-가벼운-전력-예측-모델)
    + [A. TOC](#a-toc)
    + [B. 세상에서 가장 가벼운 전력 예측 모델](#b-세상에서-가장-가벼운-전력-예측-모델)
      - [B.1. 문제 제기 & 목표 설정](#b1-문제-제기--목표-설정)
      - [B.2. 문제 정의 및 해결](#b2-문제-정의-및-해결)
      - [B.3. 데이터셋 소개 및 인사이트](#b3-데이터셋-소개-및-인사이트)
      - [B.4. 결과](#b4-결과)
    + [C. Deck](#c-deck)
    + [D. Methods Used](#d-methods-used)
    + [E. Contributing Members](#e-contributing-members)
---
### B. 세상에서 가장 가벼운 전력 예측 모델
---
![](https://i.imgur.com/3P4BoJI.jpg)
#### B.1. 문제 제기 & 목표 설정
산업통상자원부 제공 *'공공데이터 활용 BI 공모전'* 내 *'기상정보를 활용한 실시간 전력수요 예측'* 과제를 수행하던 중, 전력 수요 예측 문제 해결에 기상정보가 보편적으로 활용되는 상황임을 확인했습니다. 그러나 전력 수요 데이터가 상당히 일정한 패턴을 가지고 있다는 사실에서 다음과 같은 의문이 생겼습니다. '기상정보 없이 전력수요 예측이 가능하다면?'

지역별 관측소에서 1분 간격으로 수집되는 기상정보는 방대하며 결측 비율이 높습니다. 따라서 기상정보 없이 전력수요를 예측할 수 있다면, 결측 처리 및 전처리 비용에서 자유로운 경제적인 모델을 만들 수 있을 것입니다.
이에 따라, '과거의 패턴만으로 미래의 전력 수요 예측이 가능하다'는 가설을 설정하고, 기상정보를 활용한 모델과의 MAPE 차이가 1% 미만임을 검증하여 이 가설이 참임을 증명하고자 합니다.

#### B.2. 문제 정의 및 해결
![](https://i.imgur.com/t25ZcHm.png)

**AS-IS**
1. 방대한 양의 데이터를 수집해야 합니다.
2. 탐색적 데이터 분석을 통해 가설의 타당성을 확인해야 합니다.
3. 실험을 구성하여 가설을 검증합니다.

**TO-BE**
1. 기상 및 전력 데이터를 수집하고, 결측값 보정 및 전처리를 수행하여 방대한 데이터 양과 결측 이슈를 해결합니다.
2. 탐색적 데이터 분석을 통해 가설의 타당성을 평가합니다.
3. 실험과 대조군 데이터셋을 구성하여 학습 및 예측을 수행합니다.
4. 각 그룹의 성능을 비교하여 가설을 검증합니다.

#### B.3. 데이터셋 소개 및 인사이트
**전력수요 EDA 결과**
- 전력 수요는 명확한 계절성을 가지며, 연도에 관계없이 시간대별 패턴이 일관되게 유지됩니다.
- 전력 수요에는 폭염이나 코로나와 같은 외부 요인이 반영되며, 계절성 패턴이 안정적으로 유지됩니다.
- 전력 수요는 주로 산업 수요에 의해 영향을 받습니다.
- ACF 분석 결과, 전력 수요는 과거의 패턴에 기반한 자기회귀성을 가진 시계열 데이터임을 확인했습니다.
![](https://i.imgur.com/bEQihU7.png)

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
[세상에서 가장 가벼운 전력 수요 예측](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/blob/main/presentation/model_presentation.pptx)

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

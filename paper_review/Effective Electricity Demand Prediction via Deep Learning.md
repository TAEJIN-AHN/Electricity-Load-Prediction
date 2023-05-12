
논문명 : Effective Electricity Demand Prediction via Deep Learning

저자 : Daegun Ko, Youngmin Yoon, Jinoh Kim, Haelyong Choi

**([논문 링크](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE10818150))**

## 개요
본 논문에서는 전력수요 예측 모델 3개의 성능을 비교하고 있습니다.
1. eMLP(Error correction with Multi-Layer Perceptron)
2. ARIMA (AutoRegressive Intergreted Moving Averege)
3. CNN-LSTM

## CNN-LSTM 소개
예측 성능이 가장 우수했다는 CNN-LSTM 모델의 구성을 그림으로 나타내면 다음과 같습니다. ('기상상태'는 흐림, 맑음 등으로 당시 기후를 카테고리화한 변수임)

![CNN-LSTM 모델](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/201b4154-e74b-4594-9100-0fb9c92c3667)

## 결론
상기한 3개 모델을 비교한 결과, CNN-LSTN의 예측 성능이 가장 우수했으며, 전력 수요 예측에 있어 CNN에 사용된 기상ID 값이 가장 많은 영향을 준 것으로 파악되었습니다. 

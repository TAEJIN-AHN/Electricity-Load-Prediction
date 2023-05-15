# 용어정리

|**용어**|**의미**|
|--|--|
|순차데이터(Sequential Data)|텍스트나 시계열 데이터와 같이 순서에 의미가 있는 데이터|
|타입스텝(Time Step)|샘플을 처리하는 한 단계|
|메모리 셀(cell)|층(layer)와 동일한 의미|
|은닉상태(Hidden State)|셀의 출력|

# Simple RNN이란?
```
현재 타임스텝의 출력이 다음 타임스텝의 입력값이 되는 특징을 가진 신경망!
```
![RNN](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/09264c07-431d-41c7-b060-2f12416cf836)
![RNN](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/aee2ec56-e7e4-4f8b-bd34-551bf8079c9b)

* 입력층은 순환층의 모든 노드에 연결되며 (완전연결층과 동일함), 순환층 각 노드의 출력값은 다른 모든 노드에 연결된다.
* 기본적으로 완전연결층으로만 구성된 신경망 모델에서 노드의 결과값이 다음 타임스텝 입력값이 되는 구조가 더해졌다고 생각하면 좋을 것 같다!

# LSTM(Long Short-Term Memory)(참고한 Youtube 강의 [링크](https://www.youtube.com/watch?v=rbk9XFaoCEE))
```
단기 기억이 타입 스텝의 진행에 따라 희석되는 것을 방지하기 위해, 
즉, 오래 기억하기 위해 고안된 RNN 모델!
```

## RNN은 한계점을 가지고 있다!
* Simple RNN이 가지고 잇는 한계점 : Exploding or Vanishing Gradient
* RNN 구조에서는 Self-Feedback이 적용될 때 동일한 가중치가 계속해서 곱해지게 된다.
* 만약, 해당 가중치가 1보다 크다면 언젠가는 은닉상태의 값이 무한대로 발산하게 되고, 반대로 1보다 작다면 0에 수렴하게 되는 문제가 있다.

## LSTM이란?
![8a8ac7c1-8bac-4e89-ace8-9e28813ab635_3](https://github.com/TAEJIN-AHN/Electricity-Load-Prediction/assets/125945387/a286af5a-47f5-4e50-876d-5edc91e283f0)
* Gradient Flow를 제어할 수 있는 '밸브'역할을 한다고 생각하면 쉽다!
### STEP 1, 2 (Input Gate, Forget Gate)
* 새로운 입력과 이전 상태를 참조해서 이 정보를 얼마의 비율로 사용할 것인지를 결정
* Input Gate는 얼마나 활용할지, Forget Gate는 얼마나 잊어버릴지를 결정함
### STEP 3 (Cell State)
* Input Gate와 Forget Gate에서 결정된 내용을 적절히 섞음!
### STEP 4 (Output Gate)
* Input Gate, Forget Gate, Cell Gate의 정보를 모두 종합해서 다음 은닉상태를 결정함

# GRU란?
* GRU란 LSTM의 간소화 버전이라고 생각해도 좋으며, Cell state가 없다는 것이 차이점이다. GRU가 LSTM보다 파라미터 수가 적기 때문에 Training Time이 절약되는 장점이 있으며, LSTM과 비교하여 성능을 비교하자면 Task 마다 그 차이는 천차만별이다. (아무도 밝혀내지 못했다고 함!)

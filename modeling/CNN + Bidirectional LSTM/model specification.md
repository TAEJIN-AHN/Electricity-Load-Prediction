* 합성곱 커널 사이즈 : 3
* 합성곱 필터의 개수 : 116
* LSTM Layer의 개수 : 2개 (양방향 LSTM Layer)
* Hidden State의 개수 : 288개
* Sequence의 길이 : 2016개 (1일당 5분 간격 데이터 288개 * 일주일)
* Input Dimension(사용한 컬럼의 개수) : 58개

|분류|사용변수|
|---|---|
|기상인자 (3개) |최고기온, 최저기온, 평균일사량|
|달력정보 (54개) |요일특성(Dummy, 4개), 휴일유형 (Dummy, 14개), 월(Dummy, 12개), 시간(Dummy, 24개)|
|전력수요 (1개)|5분당 전력수요|

* 학습시간 : 약 2시간 50분 (29 epoch 학습)
* Train, Test 데이터를 미리 분리한 후, Train 데이터셋에만 Scaler를 Fit-Transform하여 학습하고 테스트 시에 Scaler로 Transform만 진행하여 Test 진행
* **TEST_MAPE : 1.879%**

# 고의적으로 r2값 낮추기
#1 r2를 음수가 아닌 0.5이하로 만들 것
#2 데이터는 건들지 말것
#3 레이어는 인풋과 아웃풋 포함해서 7개 이상
#4 batcj_size =1
#5 히든레이어의 노드는 10개 이상 100개 이하
#6 train 사이즈 75%
#7 epoch 100번이상
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

#1.데이터
x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
y = np.array([1,2,4,3,5,7,9,3,8,12,13,8, 14,15,9, 6, 17,23,21,20])

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.25, shuffle= False, random_state=100)

print(x_train) #[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15]
print(y_train) #[ 1  2  4  3  5  7  9  3  8 12 13  8 14 15  9]
print(x_test) #[16 17 18 19 20]
print(y_test) #[ 6 17 23 21 20]

#2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=1))
model.add(Dense(30))
model.add(Dense(75))
model.add(Dense(90))
model.add(Dense(50))
model.add(Dense(20))
model.add(Dense(1))

#3 컴파일,훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x_train,y_train, epochs=200, batch_size=1)

#4. 평가,예측
loss= model.evaluate(x_test, y_test) 
print("로스 :", loss)
y_predict = model.predict(x_test)
results = model.predict(x)

r2= r2_score(y_test, y_predict)
print ("R2 스코어 :",r2)


plt.scatter(x,y)
#plt.plot(x, results, color ='red')
plt.scatter(x, results, color ='red')
plt.show()

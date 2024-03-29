from sklearn.datasets import load_boston
datasets = load_boston()
# x = datasets.data
# print(datasets)
x = datasets.data
y = datasets.target
# print(x.shape) #(506,13)
# print(y.shape) #(506,)

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.9,random_state=100)
model=Sequential()
# model.add(Dense(1,input_dim=13))
model.add(Dense(10,input_shape=(13,)))      
model.add(Dense(100))
model.add(Dense(1))
model.add(Dense(100))
model.add(Dense(1))
model.add(Dense(100))
model.add(Dense(1))
model.add(Dense(100))
model.add(Dense(1))

#3.컴파일 훈련
model.compile(loss='mae',optimizer='adam')
model.fit(x_train,y_train, epochs=1000)

#4.결과예측
loss=model.evaluate(x_test,y_test)
y_predict=model.predict([x_test])
result=model.predict(x)
print("로스 :",loss)
# print("x 예측값",result)

import matplotlib.pyplot as plt

from sklearn.metrics import r2_score
r2=r2_score(y_test,y_predict)
print("R2 score",r2)
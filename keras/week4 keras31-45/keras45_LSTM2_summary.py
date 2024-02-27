import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM

#1. 데이터 
datasets = np.array([1,2,3,4,5,6,7,8,9,10])

x = np.array([[1,2,3],
              [2,3,4],
              [3,4,5],
              [4,5,6],
              [5,6,7],
              [6,7,8],
              [7,8,9],]
             )

y = np.array([4,5,6,7,8,9,10])
print(x.shape, y.shape) #(7, 3) (7,)
x = x.reshape(7,3,1)
print(x.shape, y.shape) #(7, 3, 1) (7,)


# 행무시(데이터 갯수) 열우선
#2
model =  Sequential()
#model.add(SimpleRNN(units=10, input_shape = (3,1))) #timesteps, features
# 3-D tensor with shape (batch_size, timesteps, features).
model.add(LSTM(units=10, input_shape = (3,1))) #timesteps, features
model.add(Dense(7, activation='relu'))
model.add(Dense(1))

model.summary()
# #3
# model.compile(loss = 'mse', optimizer='adam')
# model.fit(x,y, epochs=1000)

# #4
# results =  model.evaluate(x,y)
# print('loss', results)
# y_pred = np.array([8,9,10]).reshape(1,3,1)
# y_pred = model. predict(y_pred)
# print('[8,9,10]의 결과', y_pred)

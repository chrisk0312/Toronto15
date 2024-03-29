import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, f1_score
from keras.utils import to_categorical
from sklearn.preprocessing import MaxAbsScaler


#1.데이터
path= "c:\_data\dacon\dechul\\"
train_csv=pd.read_csv(path+"train.csv",index_col=0)
test_csv=pd.read_csv(path+"test.csv",index_col=0)
sample_csv=pd.read_csv(path+"sample_submission.csv")
x= train_csv.drop(['대출등급'],axis=1)
y= train_csv['대출등급']

# print(train_csv,train_csv.shape)        (96294, 14)
# print(test_csv,test_csv.shape)          (64197, 13)
# print(sample_csv,sample_csv.shape)      (64197, 2)
print(np.unique(y,return_counts=True))


y = y.values.reshape(-1,1)
# y=y.values # series -> np.array
# y =y.reshape(-1,1) #
# y = y.to_frame()

ohe = OneHotEncoder(sparse=False)
ohe = OneHotEncoder()
y_ohe = ohe.fit_transform(y).toarray()

# print(y_ohe,y_ohe.shape)


lb=LabelEncoder()
lb.fit(x['대출기간'])
x['대출기간'] = lb.transform(x['대출기간'])
lb.fit(x['근로기간'])
x['근로기간'] = lb.transform(x['근로기간'])
lb.fit(x['주택소유상태'])
x['주택소유상태'] = lb.transform(x['주택소유상태'])
lb.fit(x['대출목적'])
x['대출목적'] = lb.transform(x['대출목적'])

lb.fit(test_csv['대출기간'])
test_csv['대출기간'] =lb.transform(test_csv['대출기간'])

lb.fit(test_csv['근로기간'])
test_csv['근로기간'] =lb.transform(test_csv['근로기간'])

lb.fit(test_csv['주택소유상태'])
test_csv['주택소유상태'] =lb.transform(test_csv['주택소유상태'])

lb.fit(test_csv['대출목적'])
test_csv['대출목적'] =lb.transform(test_csv['대출목적'])

x_train,x_test,y_train,y_test=train_test_split(x,y_ohe,train_size=0.8,random_state=40,stratify=y_ohe)




scaler = MaxAbsScaler()

scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)
print(np.min(x_train))
print(np.min(x_test))
print(np.max(x_train))
print(np.max(x_test))
# print(x_train,x_test)
# print(y_train,y_test)

# x_train=np.asarray(x_train).astype(np.float32)
# x_test=np.asarray(x_test).astype(np.float32)
# test_csv = np.asarray(test_csv).astype(np.float32)


#2.모델구성
model=Sequential()
model.add(Dense(13,input_shape=(13,),activation='relu'))
model.add(Dense(26))
model.add(Dense(39))
model.add(Dense(78))
model.add(Dense(50))
model.add(Dense(7,activation='softmax'))

#3.컴파일 훈련
from keras.callbacks import EarlyStopping
es= EarlyStopping(monitor='val_loss',mode='min',patience=30,verbose=2,restore_best_weights=True)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
hist= model.fit(x_train, y_train, epochs=700,batch_size=448, validation_split=0.2,verbose=2,
          callbacks=[es]
            )




# ... (이전 코드)

#4.결과예측
loss = model.evaluate(x_test, y_test)
y_submit = model.predict(test_csv)
y_test_indices = np.argmax(y_test, axis=1)
y_submit_indices = np.argmax(y_submit, axis=1)

# 할당 전에 길이 확인
# print(len(y_test_indices), len(y_submit_indices), len(sample_csv))

# y_test_indices = np.argmax(y_test, axis=1)                        (argmax는 숫자가 제일 큰곳의 인덱스를 알려줌)
# y_submit_indices = np.argmax(y_submit, axis=1)

y_submit = ohe.inverse_transform(y_submit)
y_submit = pd.DataFrame(y_submit)
sample_csv["대출등급"]=y_submit

sample_csv.to_csv(path + "sample_submission_3.csv", index=False)

y_pred= model.predict(x_test)
y_pred= ohe.inverse_transform(y_pred)
y_test = ohe.inverse_transform(y_test)
f1=f1_score(y_test,y_pred, average='macro')


print("f1",f1)
print("로스:", loss[0])
print("acc", loss[1])


import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "c:\windows\Fonts\gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

plt.figure(figsize=(9,6))
plt.plot(hist.history['val_loss'],c='red', label='loss',marker='.')
plt.plot(hist.history['val_accuracy'],c='blue', label='acc',marker='.')
plt.legend(loc='upper right')
plt.title('wine loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid()
plt.show()

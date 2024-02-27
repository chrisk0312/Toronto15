#https://dacon.io/competitions/official/236214/data

#문자 수치화
#값 일부 자르기 (label encoder)
#값 자른거 수치화까지!

from keras.models import Sequential
from keras.layers import Dense,Dropout, BatchNormalization,Conv2D,Flatten, MaxPooling2D
import numpy as np
import pandas as pd
from sklearn.experimental import enable_halving_search_cv #정식버전이 아님!
from sklearn.model_selection import train_test_split,GridSearchCV,HalvingGridSearchCV,RandomizedSearchCV
from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler
from keras.callbacks import EarlyStopping
import sklearn as sk
import time
import warnings
warnings.filterwarnings(action='ignore')
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.ensemble import RandomForestClassifier




#1. 데이터
le = LabelEncoder()
path = "C:\\_data\\daicon\\bank\\"

train_csv = pd.read_csv(path + 'train.csv', index_col= 0)
#print(train_csv)
test_csv = pd.read_csv(path + 'test.csv', index_col= 0)
#print(test_csv)
submission_csv = pd.read_csv(path + 'sample_submission.csv')
#print(submission_csv)

# print(train_csv.shape) #(96294, 14)
# print(test_csv.shape)  #(64197, 13)
# print(submission_csv.shape) #(64197, 2)


#print(train_csv.columns) #'대출금액', '대출기간', '근로기간', '주택소유상태', '연간소득', '부채_대비_소득_비율', '총계좌수', '대출목적',
#       '최근_2년간_연체_횟수', '총상환원금', '총상환이자', '총연체금액', '연체계좌수', '대출등급'

#대출기간 처리
train_loan_time = train_csv['대출기간']
train_loan_time = train_loan_time.str.split()
for i in range(len(train_loan_time)):
    train_loan_time.iloc[i] = int((train_loan_time)[i][0])
    
#print(train_loan_time)   

test_loan_time = test_csv['대출기간']
test_loan_time = test_loan_time.str.split()
for i in range(len(test_loan_time)):
    test_loan_time.iloc[i] = int((test_loan_time)[i][0])

#print(test_loan_time)   

train_csv['대출기간'] = train_loan_time
test_csv['대출기간'] = test_loan_time



#print(test_csv)


#근로기간 처리
train_working_time = train_csv['근로기간']
test_working_time = test_csv['근로기간']

for i in range(len(train_working_time)):
    data = train_working_time.iloc[i]
    if data == 'Unknown':
        train_working_time.iloc[i] = np.NaN
    elif data == '10+ years' or data == '10+years':
        train_working_time.iloc[i] = int(15)
    elif data == '< 1 year' or data == '<1 year':
        train_working_time.iloc[i] = int(0.6)
    else:
        train_working_time.iloc[i] = int(data.split()[0])
        
    
train_working_time = train_working_time.fillna(train_working_time.mean())

#print(train_working_time)

for i in range(len(test_working_time)):
    data = test_working_time.iloc[i]
    if data == 'Unknown':
        test_working_time.iloc[i] = np.NaN
    elif data == '10+ years' or data == '10+years':
        test_working_time.iloc[i] = int(15)
    elif data == '< 1 year' or data == '<1 year':
        test_working_time.iloc[i] = int(0.6)
    else:
        test_working_time.iloc[i] = int(data.split()[0])
    
test_working_time = test_working_time.fillna(test_working_time.mean())

train_csv['근로기간'] = train_working_time
test_csv['근로기간'] = test_working_time 
#print(test_csv['근로기간'])
#print(train_csv['근로기간'])




#대출목적 전처리
test_loan_perpose = test_csv['대출목적']
train_loan_perpose = train_csv['대출목적']



for i in range(len(test_loan_perpose)):
    data = test_loan_perpose.iloc[i]
    if data == '결혼':
        test_loan_perpose.iloc[i] = np.NaN
        

for i in range(len(test_loan_perpose)):
    data = test_loan_perpose.iloc[i]
    if data == '기타':
        test_loan_perpose.iloc[i] = np.NaN
               
for i in range(len(train_loan_perpose)):
    data = train_loan_perpose.iloc[i]
    if data == '기타':
        train_loan_perpose.iloc[i] = np.NaN
        

test_loan_perpose = test_loan_perpose.fillna(method='ffill')
train_loan_perpose = train_loan_perpose.fillna(method='ffill')


test_csv['대출목적'] = test_loan_perpose
train_csv['대출목적'] = train_loan_perpose







######## 결측치확인
# print(test_csv.isnull().sum()) #없음.
# print(train_csv.isnull().sum()) #없음.





#print(np.unique(test_loan_perpose))  #'기타' '부채 통합' '소규모 사업' '신용 카드' '의료' '이사' '자동차' '재생 에너 
#지' '주요 구매' '주택'
# '주택 개선' '휴가'







le.fit(train_csv['주택소유상태'])
train_csv['주택소유상태'] = le.transform(train_csv['주택소유상태'])
le.fit(test_csv['주택소유상태'])
test_csv['주택소유상태'] = le.transform(test_csv['주택소유상태'])
#print(train_csv['주택소유상태'])
#print(test_csv['주택소유상태'])


le.fit(train_csv['대출목적'])
train_csv['대출목적'] = le.transform(train_csv['대출목적'])
le.fit(test_csv['대출목적'])
test_csv['대출목적'] = le.transform(test_csv['대출목적'])

le.fit(train_csv['대출기간'])
train_csv['대출기간'] = le.transform(train_csv['대출기간'])
le.fit(test_csv['대출기간'])
test_csv['대출기간'] = le.transform(test_csv['대출기간'])





x = train_csv.drop(['대출등급'], axis = 1)


#print(x)
y = train_csv['대출등급']


y = le.fit_transform(y)



# ohe = OneHotEncoder(sparse = False)
# ohe.fit(y)
# y_ohe = ohe.transform(y)
# print(y_ohe.shape)  


     
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.preprocessing import StandardScaler, RobustScaler

mms = MinMaxScaler(feature_range=(1,3))
#mms = StandardScaler()
#mms = MaxAbsScaler()
#mms = RobustScaler()

mms.fit(x)
x = mms.transform(x)
test_csv=mms.transform(test_csv)
#print(x.shape, y.shape)  #(96294, 13) (96294, 7)
#print(np.unique(y, return_counts= True)) #array(['A', 'B', 'C', 'D', 'E', 'F', 'G'], dtype=object), array([16772, 28817, 27623, 13354,  7354,  1954,   420],

#print(train_csv)

#print(y.shape) #(96294,)
#print(np.unique(y, return_counts= True)) #Name: 근로기간, Length: 96294, dtype: float64


x_train, x_test, y_train, y_test = train_test_split(x, y, train_size= 0.88,  shuffle= True, random_state= 279, stratify= y) #170 #279 

# smote = SMOTE(random_state=270,sampling_strategy='auto',k_neighbors=10,)
# x_train, y_train =smote.fit_resample(x_train, y_train)




# from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
# from sklearn.preprocessing import StandardScaler, RobustScaler, Normalizer

# #mms = MinMaxScaler(feature_range=(1,5))
# mms = StandardScaler()
# #mms = MaxAbsScaler()
# #mms = RobustScaler()


parameters = [
    {"RF__n_estimators": [100, 200], "RF__max_depth": [6, 10, 12], "RF__min_samples_leaf": [3, 10]},
    {"RF__max_depth": [6, 8, 10, 12], "RF__min_samples_leaf": [3, 5, 7, 10]},
    {"RF__min_samples_leaf": [3, 5, 7, 10], "RF__min_samples_split": [2, 3, 5, 10]},
    {"RF__min_samples_split": [2, 3, 5, 10]},
]    
     


#2. 모델구성
     
#model = RandomForestClassifier()


#model = make_pipeline(MinMaxScaler(), RandomForestClassifier())
pipe = Pipeline([('mm',MinMaxScaler()),('RF',RandomForestClassifier())])
 
#model = GridSearchCV(pipe, parameters, cv=5, verbose=1)
#model = RandomizedSearchCV(pipe, parameters, cv=5, verbose=1)
model = HalvingGridSearchCV(pipe, parameters, cv=5, verbose=1)




#3. 컴파일, 훈련

import datetime
date= datetime.datetime.now()
date = date.strftime("%m%d-%H%M") #m=month, M=minutes

path1= 'C:/_data/_save/MCP/_k28/' #경로(스트링data (문자))
filename = '{epoch:04d}-{val_loss:.4f}.hdf5' #filename= 에포4자리수-발로스는 소숫점4자리까지 표시. 예)1000-0.3333.hdf5
filepath = "".join([path1, 'k28_11_', date, "_", filename]) #""공간에 ([])를 합쳐라.


x_train = np.asarray(x_train).astype(np.float32)
x_test = np.asarray(x_test).astype(np.float32)
test_csv = np.asarray(test_csv).astype(np.float32)



start_time = time.time()
model.fit(x_train, y_train)
end_time = time.time()


#4. 평가, 예측

results = model.score(x_test, y_test)
print("로스 :", results)
print("걸린 시간 :", round(end_time - start_time, 2), "초")


y_predict = model.predict(x_test )

y_submit = model.predict(test_csv)


f1 = f1_score(y_test,y_predict,average='macro')
print("F1: ",f1)



import datetime
dt = datetime.datetime.now()
submission_csv['대출등급'] = y_submit

submission_csv.to_csv(path+f"submit_{dt.day}day{dt.hour:2}{dt.minute:2}_F1_{f1:4}.csv",index=False)



#minmax
#로스 : 0.45476970076560974
#정확도 : 0.8460853695869446

#mms = StandardScaler()

#로스 : 0.46329641342163086
#정확도 : 0.8380373120307922

#mms = MaxAbsScaler()
#로스 : 0.44124674797058105
#F1:  0.8497932009729917


#mms = RobustScaler()
#로스 : 0.3884388208389282
#F1:  0.865791228309671



#LinearSVC
# 로스 : 0.3806680512287989
# 걸린 시간 : 47.78 초
# F1:  0.1864885248672083

#pipeline
# 로스 : 0.8142090688819661
# 걸린 시간 : 7.1 초
# F1:  0.6915816805313789

#pipe2
# 로스 : 0.8083246798200069
# 걸린 시간 : 237.2 초
# F1:  0.6804647109777529
import numpy as np
import pandas as pd #판다스에 데이터는 넘파이 형태로 들어가있음.
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_squared_log_error, accuracy_score
import time
from keras.callbacks import EarlyStopping
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Perceptron
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split,KFold,cross_val_score, StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from xgboost import XGBClassifier, XGBRegressor

#1. 데이터
path = "C:\\_data\\kaggle\\bike\\"


train_csv = pd.read_csv(path + "train.csv", index_col=0)
print(train_csv)
test_csv = pd.read_csv(path + "test.csv", index_col= 0)
print(test_csv)
submission_csv = pd.read_csv(path + "sampleSubmission.csv")
print(submission_csv)

print(train_csv.columns)
# ['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp',
#       'humidity', 'windspeed', 'casual', 'registered', 'count']

print(train_csv.info())
print(test_csv.info())


x = train_csv.drop(['casual','registered','count'], axis=1)
print(x)
y = train_csv['count']
print(y)

print(train_csv.index)
from sklearn.model_selection import train_test_split,KFold,cross_val_score, GridSearchCV, RandomizedSearchCV
x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle= True, random_state= 123, train_size=0.8)
scaler = MinMaxScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)


n_splits=5
kfold = KFold(n_splits=n_splits, shuffle=True, random_state=123)
#n_split = 섞어서 분할하는 갯수
#kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=123)


#2. 모델구성
parameters = [
    {"n_estimators": [500, 200], "max_depth": [6, 10, 12], "min_samples_leaf": [3, 10], "gamma": [0,2,4]},
    {"max_depth": [8, 10, 12], "min_samples_leaf": [3, 5, 7, 10],"gamma": [0,2,4]},
    {"min_samples_leaf": [3, 5, 7, 10], "min_samples_split": [2, 3, 5, 10],"gamma": [0,2,4]},
    {"min_samples_split": [2, 3, 5, 10], "subsample": [0, 0.3, 1],"gamma": [0,2,4]},
    {"reg_alpha": [0.2351, 0.135], "min_samples_split": [2, 3, 5, 10], "max_depth" : [4, 8, 10, 11]}]



model = RandomizedSearchCV(XGBRegressor(),
                              parameters,
                              cv = kfold,
                              verbose = 1,
                               refit= True,
                               random_state= 123,
                               n_jobs= 22)

start_time = time.time()
model.fit(x_train, y_train)
end_time = time.time()


best_predict = model.best_estimator_.predict(x_test)
best_r2_score = r2_score(y_test, best_predict)

print("최적의 매개변수 : ", model.best_estimator_)
print("최적의 파라미터 : ", model.best_params_)
print('best_score :', model.best_score_)
print('score :', model.score(x_test, y_test))

y_predict = model.predict(x_test)
print("r2_score :", r2_score(y_test, y_predict))

y_pred_best = model.best_estimator_.predict(x_test)
print("최적튠 r2 :", r2_score(y_test, y_predict))

print("걸린시간 :", round(end_time - start_time, 2), "초")

# 최적의 매개변수 :  RandomForestRegressor(max_depth=10, min_samples_leaf=3, n_estimators=200)
# 최적의 파라미터 :  {'max_depth': 10, 'min_samples_leaf': 3, 'n_estimators': 200}
# best_score : 0.3551549732336853
# score : 0.3376106650596302
# 걸린시간 : 28.32 초

#randomizer
# 최적의 매개변수 :  RandomForestRegressor(max_depth=10, min_samples_leaf=7)
# 최적의 파라미터 :  {'min_samples_leaf': 7, 'max_depth': 10}
# best_score : 0.3542598232660622
# score : 0.3332154501608132
# 걸린시간 : 3.95 초
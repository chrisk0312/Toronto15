from sklearn.datasets import load_digits
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,KFold,cross_val_score, StratifiedKFold, cross_val_predict, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from xgboost import XGBClassifier, XGBRegressor

datasets = load_digits() #mnist 원판
x = datasets.data
y = datasets.target
print(x)
print(y)

print(x.shape) #(1797, 64)
print(y.shape) #(1797,)
print(pd.value_counts(y, sort= False)) #sort= False 제일 앞 데이터부터 순서대로 나옴
# 0    178
# 1    182
# 2    177
# 3    183
# 4    181
# 5    182
# 6    181
# 7    179
# 8    174
# 9    180

x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, random_state=123, stratify=y)



models = [DecisionTreeRegressor(), RandomForestRegressor(), GradientBoostingRegressor(), XGBRegressor()]

for model in models:
    model.fit(x_train, y_train)
    results = model.score(x_test,y_test) #분류에서는 (디폴트값)acc 빼줌 회귀는 r2
    y_predict = model.predict(x_test)
    r2 = r2_score(y_predict, y_test)
    print(type(model).__name__, "r2 :", r2)
    print(type(model).__name__, ':', model.feature_importances_)
        


y_predict = model.predict(x_test)
print("acc_score", accuracy_score(y_test, y_predict))


y_pred_best = model.best_estimator_.predict(x_test)
print("최적튠 ACC :", accuracy_score(y_test, y_predict))


#randomforest
# acc_score 0.9866666666666667
# 걸린시간 : 0.14 초

#RandomsearchCV
# acc_score 0.98
# 최적의 매개변수 :  RandomForestClassifier(min_samples_leaf=3, min_samples_split=5, n_jobs=-1)
# 최적의 파라미터 :  {'n_jobs': -1, 'min_samples_split': 5, 'min_samples_leaf': 3}
# best_score : 0.965857083849649
# score : 0.98
# 최적튠 ACC : 0.98
# 걸린시간 : 1.74 초

#GridSearchCV
# acc_score 0.9866666666666667
# 최적의 매개변수 :  RandomForestClassifier(min_samples_split=3, n_jobs=-1)
# 최적의 파라미터 :  {'min_samples_split': 3, 'n_jobs': -1}
# best_score : 0.9725237505163156
# score : 0.9866666666666667
# 최적튠 ACC : 0.9866666666666667
# 걸린시간 : 17.16 초

# DecisionTreeRegressor r2 : 0.6799216169762554
# DecisionTreeRegressor : [0.00000000e+00 1.16612822e-03 5.09626480e-03 3.84660352e-04
#  1.46337353e-02 4.46549263e-03 2.42593236e-03 7.07695280e-03
#  0.00000000e+00 8.67371382e-05 5.10131430e-03 8.91167527e-03
#  2.97700954e-02 1.47821126e-02 0.00000000e+00 6.03388787e-05
#  2.12743176e-03 1.17660814e-03 8.33005221e-03 1.73368241e-02
#  9.07539503e-02 6.61954596e-02 0.00000000e+00 4.52541590e-05
#  8.95026701e-05 1.94655408e-03 1.56379266e-02 3.25710728e-02
#  1.08229070e-02 4.77529349e-02 1.99653929e-02 0.00000000e+00
#  0.00000000e+00 2.08994247e-02 5.59505259e-02 4.36674959e-02
#  9.39997499e-02 1.66858813e-02 2.02187448e-02 0.00000000e+00
#  0.00000000e+00 7.09611840e-03 8.10598704e-02 1.07226972e-02
#  1.92039804e-03 5.45312617e-03 5.28079989e-03 0.00000000e+00
#  0.00000000e+00 8.92684781e-05 8.93328854e-05 1.17951897e-02
#  1.32048549e-01 1.08099103e-02 5.47723478e-03 0.00000000e+00
#  0.00000000e+00 0.00000000e+00 4.97946597e-04 4.97871173e-03
#  7.38774146e-03 4.38873920e-04 5.44801550e-02 2.38941960e-04]
# RandomForestRegressor r2 : 0.8180254433139127
# RandomForestRegressor : [0.00000000e+00 6.18661361e-04 3.56300711e-03 3.29675248e-03
#  5.94643748e-03 9.03607638e-03 2.71015283e-03 8.10092460e-04
#  3.02526076e-05 3.42758707e-03 9.74644864e-03 5.25541640e-03
#  4.04107157e-02 1.71253317e-02 4.34974398e-03 2.73516174e-04
#  1.48100322e-04 3.06288917e-03 1.91572007e-02 1.17984418e-02
#  7.57930904e-02 6.22110715e-02 6.94569459e-03 1.87521665e-04
#  1.39667620e-04 5.86228321e-03 2.46142936e-02 3.94647135e-02
#  5.49262208e-02 4.85239613e-02 1.32492969e-02 1.12129575e-04
#  0.00000000e+00 2.22603815e-02 2.92060059e-02 2.76951024e-02
#  1.03129915e-01 8.27896080e-03 1.23811255e-02 0.00000000e+00
#  0.00000000e+00 2.29804139e-03 3.46941144e-02 1.84815321e-02
#  5.87367268e-03 5.54524819e-03 8.04240039e-03 5.83575241e-05
#  8.42052374e-06 9.51867813e-04 4.42805453e-03 1.24893242e-02
#  1.28765204e-01 7.52891170e-03 7.50491439e-03 3.07538517e-04
#  0.00000000e+00 1.25387161e-03 6.19716462e-03 5.55061169e-03
#  1.26205096e-02 1.22548332e-02 3.48574150e-02 1.45397317e-02]
# GradientBoostingRegressor r2 : 0.7716257793542721
# GradientBoostingRegressor : [0.00000000e+00 1.65986977e-04 2.65718391e-03 5.78717323e-03
#  3.15809952e-03 4.39804707e-03 2.92745109e-03 3.10767637e-04
#  1.66332907e-04 2.23680049e-03 6.41418311e-03 1.92293544e-03
#  4.36440156e-02 8.50203157e-03 4.08663995e-03 0.00000000e+00
#  2.37515800e-04 9.76092800e-04 2.36497938e-02 1.34283343e-02
#  7.71696584e-02 5.79943780e-02 1.48121472e-02 0.00000000e+00
#  4.93302991e-05 7.42057808e-03 8.20229280e-03 6.93014721e-02
#  3.20855830e-02 4.84620173e-02 2.95539958e-02 7.91021947e-04
#  0.00000000e+00 3.76177914e-02 2.43786567e-02 6.46576350e-02
#  1.08961318e-01 5.38521702e-03 4.78679329e-03 0.00000000e+00
#  0.00000000e+00 1.61807885e-04 2.98911266e-02 1.38952084e-02
#  2.23252707e-03 7.83762703e-03 4.82978212e-03 0.00000000e+00
#  0.00000000e+00 4.54103439e-04 3.78013916e-03 2.43731725e-02
#  1.15842032e-01 7.63661033e-03 4.82929790e-03 2.41851117e-04
#  0.00000000e+00 1.29764100e-04 3.71976786e-03 2.35370815e-04
#  1.92548282e-02 1.65634370e-02 1.67040377e-02 1.10882372e-02]
# XGBRegressor r2 : 0.85270463189354
# XGBRegressor : [0.00000000e+00 2.39726249e-03 1.18899811e-03 4.85838763e-03
#  2.95385858e-03 9.97265615e-03 6.70667365e-03 3.23929563e-02
#  3.82048846e-03 8.99295497e-04 8.48939456e-03 4.72026970e-03
#  2.25541238e-02 5.97741269e-03 4.02598968e-03 2.49898658e-05
#  4.24577564e-04 5.51048899e-03 1.21178171e-02 7.70156737e-03
#  6.17719218e-02 3.76914032e-02 2.46904138e-03 2.13046155e-06
#  0.00000000e+00 6.78864121e-03 9.34198964e-03 2.30608340e-02
#  2.28433106e-02 4.98778932e-02 1.40471673e-02 0.00000000e+00
#  0.00000000e+00 5.63976839e-02 3.62221599e-02 2.86378134e-02
#  8.20513740e-02 1.48464795e-02 1.58700235e-02 0.00000000e+00
#  0.00000000e+00 3.03022587e-03 5.86998388e-02 1.34973321e-02
#  9.15888324e-03 8.21406208e-03 4.78263339e-03 1.77108537e-04
#  0.00000000e+00 6.84757368e-04 2.42394209e-03 1.18598351e-02
#  9.70579013e-02 1.04145110e-02 1.33812707e-02 5.88691728e-05
#  0.00000000e+00 2.49125506e-03 2.50026607e-03 7.34606944e-03
#  1.59468893e-02 2.57708551e-03 7.21126497e-02 6.49275482e-02]
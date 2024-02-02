import numpy as np
from keras.datasets import mnist
import pandas as pd
(x_train,y_train),(x_test,y_test)= mnist.load_data()
print(x_train.shape, y_train.shape) #(60000, 28, 28) (60000,)
print(x_train.shape, y_test.shape)  #(60000, 28, 28) (10000,)

print(x_train)
print(x_train[0]) 
print(y_train[0]) #5
print(np.unique(y_train, return_counts=True))
# The np.unique() function is used to find the unique elements of an array.
# When used with the return_counts=True argument,
# it also returns the count of each unique element.
# This line will print two arrays. The first array is the sorted unique values in y_train. 
# The second array is the count of each of these unique values in y_train.
# This is particularly useful in a classification problem to understand the distribution of classes in your training set.


# (array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=uint8), array([5923, 6742, 5958, 6131, 5842, 5421, 5918, 6265, 5851, 5949],
#       dtype=int64))
print(pd.value_counts(y_test))

import matplotlib.pyplot as plt
plt.imshow(x_train[0],'spring')
plt.show()

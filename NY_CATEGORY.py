import pandas as pd
import dataset_places_cleaning
import numpy as np

ratings = pd.read_csv('dataset_TSMC2014_NYC.csv')
ratings = ratings[:100000]
num_users = ratings['userId'].max()
num_distance = ratings['cat_id'].max()
num_movies
rating_matrix = np.zeros((num_users+1,num_movies+1))
for i in range(ratings.shape[0]):
    index = ratings[i:i+1]
    row = int(index['userId'])
    col = int(index['cat_id'])
    val = int(index['rating'])
    rating_matrix[row][col] = val
from sklearn import cross_validation
train,test = cross_validation.train_test_split(rating_matrix)
train.shape
import sklearn.metrics
distance = 1-sklearn.metrics.pairwise.cosine_distances(train)
user_pred = distance.dot(train).T/np.array(np.abs(distance).sum(axis = 1)).T
user_pred.shape
train.shape
def get_mse(pred,actual):
    pred   = pred.flatten()
    actual = actual.flatten()
    return pred,actual
a,b = get_mse(user_pred,train)
print(a.shape)
print(b.shape)
error = sklearn.metrics.mean_squared_error(a,b)
error = 100-error
print("Accuracy - " , error ,"%" )
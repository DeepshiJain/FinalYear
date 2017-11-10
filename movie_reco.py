
import numpy as np
import pandas as pd

header = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=header)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]
print('Number of users = %s and Number of movies = %s' % (str(n_users),str(n_items)))

from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(df, test_size=0.25)

#print(type(train_data))

# Create two user-item matrices, one for training and another for testing
#train_data = train_data.reset_index();
#test_data = test_data.reset_index();
#print(train_data)

n_train = train_data.shape[0];
n_test = test_data.shape[0];

train_data_matrix = np.zeros((n_users, n_items))
#print(train_data)
i=0
#print("Getting single value....")
#print(train_data.iat[1,1])
while i<n_train:
    #print(train_data.index[i])
    #train_data_matrix[train_data.get_value(train_data.index[i],'user_id') - 1, train_data.get_value(train_data.index[i],'item_id') - 1] = train_data.get_value(train_data.index[i],'rating')
    train_data_matrix[train_data.iat[i,0] - 1, train_data.iat[i,1] - 1] = train_data.iat[i,2]
    i = i+1

test_data_matrix = np.zeros((n_users, n_items))
i = 0
while i<n_test:
    #print(test_data.index[i])
    #test_data_matrix[test_data.get_value(test_data.index[i],'user_id') - 1, test_data.get_value(test_data.index[i],'item_id') - 1] = test_data.get_value(test_data.index[i],'rating')
    test_data_matrix[test_data.iat[i,0] - 1, test_data.iat[i,1] - 1] = test_data.iat[i,2]
    i = i+1

from sklearn.metrics.pairwise import pairwise_distances

user_similarity = pairwise_distances(train_data_matrix, metric='cosine')


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        return pred


user_prediction = predict(train_data_matrix, user_similarity, type='user')

#print(user_prediction)

from sklearn.metrics import mean_squared_error
from math import sqrt


def rms_error(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


print('User-based CF RMSE: %s' % str(rms_error(user_prediction, test_data_matrix)))

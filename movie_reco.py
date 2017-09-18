import numpy as np
import pandas as pd

header = ['user_id', 'item_id', 'rating', 'timestamp']
dfx = pd.read_csv('u.data', sep='\t')
df = pd.read_csv('u.data', sep='\t', names=header)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]

#n_users = "4"
#n_items = "5"
print('Number of users is {0} | Number of movies is {1}'.format(n_users,n_items))

#from sklearn import cross_validation as cv

from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(dfx, test_size=0.25)

print(train_data)

print("Hello there is test data...")

#print(train_data.user_id)

#print(test_data)
# Create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_items))
#n_train_data = train_data.user_id.shape[0]
x = 1
#while (x<=n_train_data):
#    train_data_matrix[train_data.user_id]
for line in train_data:
    #if x < 6:
        #x = x+1
        #continue
        #print(line[0])
        #print(line[1])
        #print(line[2])
        #continue
    #train_data_matrix[line[0] - 1, line[1] - 1] = line[2]
    print(line[0])
    print(line[1])
    print(line[2])
    print("....done...")

test_data_matrix = np.zeros((n_users, n_items))
x = 1
for line in test_data:
    if x < 2:
        x = 2
        continue
    #test_data_matrix[line[0] - 1, line[1] - 1] = line[2]

from sklearn.metrics.pairwise import pairwise_distances

user_similarity = pairwise_distances(train_data_matrix, metric='cosine')


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
            [np.abs(similarity).sum(axis=1)]).T
        return pred


user_prediction = predict(train_data_matrix, user_similarity, type='user')

from sklearn.metrics import mean_squared_error
from math import sqrt


def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


#print 'User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))

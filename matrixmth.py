import pandas as pd
import numpy as np

ratings_list = [i.strip().split("::") for i in open('ml-1m/ratings.dat', 'r').readlines()]
users_list = [i.strip().split("::") for i in open('ml-1m/users.dat', 'r').readlines()]
movies_list = [i.strip().split("::") for i in open('ml-1m/movies.dat', 'r').readlines()]

ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = int)
movies_df = pd.DataFrame(movies_list, columns = ['MovieID', 'Title', 'Genres'])
movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric)

print(movies_df.head())
R_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)
#print("R_df printing")
#print(R_df.head())

R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

# for singular value decomposition
from scipy.sparse.linalg import svds

U, sigma, Vt = svds(R_demeaned, k=50)
sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)


def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
	#sorting user's predictions
	user_row_number = userID - 1
	sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

	#merging user's data in the movie information.
	user_data = original_ratings_df[original_ratings_df.UserID == (userID)]
	user_full = (user_data.merge(movies_df, how='left', left_on='MovieID', right_on='MovieID').
				 sort_values(['Rating'], ascending=False)
				 )

	print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
	print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))

	recommendations = (movies_df[~movies_df['MovieID'].isin(user_full['MovieID'])].
					   merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
							 left_on='MovieID',
							 right_on='MovieID').
					   rename(columns={user_row_number: 'Predictions'}).
					   sort_values('Predictions', ascending=False).
					   iloc[:num_recommendations, :-1]
					   )

	return user_full, recommendations


already_rated, predictions = recommend_movies(preds_df, 837, movies_df, ratings_df, 10)

print ("Already Rated by user....")
print(already_rated.head(10))

print("Predictions for that user....")
print(predictions)

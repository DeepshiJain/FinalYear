#!/usr/bin/env python

# import argparse
import csv
import operator
#import sys
# import numpy
from collections import OrderedDict
# import pickle

#create support lookup table
#movieID - Rating(0.5-5.0) - Count - %



def fun1(input_file):

	#['userId', 'movieId', 'rating', 'timestamp']

	input_data = open(input_file, "r").readlines()[1:]
	input_user = []
	input_movie_and_ratings = []
	for ln in input_data:
		ln = ln.split(",")
		input_movie_and_ratings.append([ln[1], ln[2].strip()])  # [float(ln[1]), float(ln[2])])
		if ln[0] not in input_user:
			input_user.append(ln[0])  # int(ln[0]))
	#print ("Movie-Rating Tuples: %s" % str(input_movie_and_ratings))
	#print ("Input User(s): %s" % str(input_user))

	ratings = open("../data/ml-ratings-100k-sample.csv", "r").readlines()[1:]
	#ratings = numpy.loadtxt(open("ml-ratings-lean.csv","rb"), delimiter=",", skiprows=1)
	f = open("../data/output/a1-ratings-extract.csv", "w")

	#count = 0
	#total = float(len(ratings))

	for ln in ratings:
		#count += 1  # Progress Bar
		#p = count / total * 100.0
		#sys.stdout.write("\rRatings processed: %d (%i)" % (count, p))
		#sys.stdout.flush()
		ln2 = ln.split(",")
		pair = [ln2[1], ln2[2].strip()]  # strip removes spaces after

		#print(pair)
		#  if pair in input_movie_and_ratings and ratings[ln][0] not in input_user:
		if pair in input_movie_and_ratings and ln2[0] not in input_user:
			with open("../data/output/a1-ratings-extract.csv", "a") as f:
				f.write(ln)

	print ("\nDone fun1\n")


def fun2():
	
	data = open("../data/output/a1-ratings-extract.csv", "r").readlines()
	ratings_count = 1
	ratings_count_list = []
	ratings_count_list_uniques = []

	f = open("../data/output/a2-ratings-extract-counts-by-user.csv", "w")

	for n in range(0, len(data)):
		row1 = data[n].split(",")
		try:
			row2 = data[n + 1].split(",")
		except IndexError:  # exception thrown when file reaches end of line
			#print ("Max Agreement: %s" % str(max(ratings_count_list)))
			ratings_count_list_uniques.sort()
			print ("Freqs Present: %s" % str(ratings_count_list_uniques))

		user_id1 = row1[0]
		user_id2 = row2[0]

		if user_id1 == user_id2:
			ratings_count += 1
		if user_id1 != user_id2:

			with open("../data/output/a2-ratings-extract-counts-by-user.csv", "a") as f:
				f.write(user_id1 + "," + str(ratings_count) + "\n")
				ratings_count_list.append(ratings_count)
				if ratings_count not in ratings_count_list_uniques:
					ratings_count_list_uniques.append(ratings_count)
			ratings_count = 1

	output = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()
	print ("Total output Rows: %s" % str(len(output)))


	output = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()

	count_dict = {}
	for n in range(0, len(output)):
		row1 = output[n].split(",")

		count1 = int(row1[1].strip())

		if count1 not in count_dict:
			count_dict[count1] = 0
		if count1 in count_dict:
			count_dict[count1] += 1

	OrderedDict(sorted(count_dict.items(), key=lambda t: t[0]))
	print ("Distribution : %s" % str(count_dict))

	f = open("../data/output/a2-ratings-extract-counts-by-user-distrib.csv", "w")
	for i in count_dict:
		with open("../data/output/a2-ratings-extract-counts-by-user-distrib.csv", "a") as f:
			f.write(str(i) + ',' + str(count_dict[i]) + '\n')

	print ("Done fun2\n")


def fun3(lower_limit=6, upper_limit=8):
	
	data = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()
	agreeing_users = []

	for n in range(0, len(data)):
		row1 = data[n].split(",")
		count = int(row1[1].strip())

		if lower_limit <= count and count <= upper_limit:
			agreeing_users.append(row1[0])

	#print ("Users ( %s ): %s"% str(len(agreeing_users)),str(agreeing_users))

	f = open("../data/output/a3-userids-extract-agreeing-users.csv", "w")
	for row in agreeing_users:
		with open("../data/output/a3-userids-extract-agreeing-users.csv", "a") as f:
			f.write(row + '\n')

	print ("Done fun3\n")


def fun4():
	
	# ratings_extract = open("a1-ratings-extract.csv", "r").readlines()
	ratings = open("../data/ml-ratings-100k-sample.csv", "r").readlines()
	agreeing_users_extract = open("../data/output/a3-userids-extract-agreeing-users.csv", "r").readlines()
	input_data = open("../data/input/v1-input-ratings.csv", "r").readlines()  #exp-2-input.csv
	input_data = input_data[1:]

	input_movie_and_ratings = []
	for ln in input_data:
		ln = ln.split(",")
		input_movie_and_ratings.append([ln[1], ln[2]])

	agreeing_users = []
	for ln in agreeing_users_extract:
		agreeing_users.append(ln.strip())
	print ("Number of Users: %s" % str(len(agreeing_users)))

	#count = 0
	f = open("../data/output/a4-ratings-extract-recommended.csv", "w")
	for ln in ratings:
		ln2 = ln.split(",")
		#count += 1
		#sys.stdout.write("\rRatings processsed: %i" % count)
		#sys.stdout.flush()

		pair = [ln2[1], ln2[2]]

		if ln2[0] in agreeing_users and pair not in input_movie_and_ratings:
			with open("../data/output/a4-ratings-extract-recommended.csv", "a") as f:
				f.write(ln)

	print ("\nDone fun4\n")


def fun5():
	
	data = []
	with open("../data/output/a4-ratings-extract-recommended.csv", "r") as f:
		for row in csv.reader(f):
			data.append(row)
	data.sort(key=operator.itemgetter(1))  # Column to sort
	with open("../data/output/a5-ratings-extract-recommended-sorted.csv", "w") as f:
		csv.writer(f).writerows(data)


	output = open("../data/output/a5-ratings-extract-recommended-sorted.csv", "r").readlines()
	count_dict = {}
	for n in range(0, len(output)):
		row1 = output[n].split(",")
		count1 = int(row1[1].strip())

		if count1 not in count_dict:
			count_dict[count1] = 0
		if count1 in count_dict:
			count_dict[count1] += 1
	OrderedDict(sorted(count_dict.items(), key=lambda t: t[0]))

	f = open("../data/output/a5-ratings-extract-recommended-sorted-counts.csv", "w")
	for i in count_dict:
		with open("../data/output/a5-ratings-extract-recommended-sorted-counts.csv", "a") as f:
			f.write(str(i) + ',' + str(count_dict[i]) + '\n')

	print ("Number of Movie-Rating Tuples: %s" % str(len(count_dict)))

	print ("Done fun5\n")


def fun6(min_ratings=10):
	
	min_rated_movies = []
	with open("../data/output/a5-ratings-extract-recommended-sorted-counts.csv", "r") as f:
		for row in csv.reader(f):
			if int(row[1]) >= min_ratings:
				min_rated_movies.append(row[0])

	print ("Sample of Movies (5): %s" % str(min_rated_movies[:5]))
	print ("Number of agreeing Movies: %s" % str(len(min_rated_movies)))

	extracted_ratings = open("../data/output/a5-ratings-extract-recommended-sorted.csv", "r").readlines()

	#count = 0
	temp_movie_ratings_sum = 0.0
	temp_movie_counts = 0
	temp_movie_avg = 0

	f = open("../data/output/a6-movies-extract-recommended.csv", "w")
	for n in range(0, len(extracted_ratings)):
		#count += 1  # Progress Bar
		#sys.stdout.write("\rRatings processsed: %i" % count)
		#sys.stdout.flush()

		row1 = extracted_ratings[n].split(",")
		try:
			row2 = extracted_ratings[n + 1].split(",")
		except IndexError:  # exception thrown when file reaches end of line
			print ("\n")   #End of Input

		movie1 = row1[1]
		movie2 = row2[1]
		temp_rating_delta = float(row1[2])

		if movie1 in min_rated_movies and movie2 == movie1:  # If next row is same movie as current row
			temp_movie_ratings_sum += temp_rating_delta
			temp_movie_counts += 1

		if movie1 in min_rated_movies and movie2 != movie1:
			temp_movie_ratings_sum += temp_rating_delta
			temp_movie_counts += 1

			temp_movie_avg = temp_movie_ratings_sum / temp_movie_counts  # Avg upon movie switch
			with open("../data/output/a6-movies-extract-recommended.csv", "a") as f:
				f.write(str(movie1) + ',' + str(temp_movie_avg) + ',' + str(temp_movie_counts) + '\n')

			temp_movie_ratings_sum = 0
			temp_movie_counts = 0

	print ("Done fun6\n")


def fun7(min_avg_rating=4.0):
	
	movies = open("../data/ml-movies.csv", "r").readlines()
	rec_data = open("../data/output/a6-movies-extract-recommended.csv", "r").readlines()

	with open("../data/output/a7-movies-extract-recommended-films.csv", "w") as f:
		f.write(','.join(['movieId', 'avgRating', 'agreeCount', 'title', 'genres', '\n']))

	#count = 0
	for ln in rec_data:
		#count += 1  # Progress Bar
		#sys.stdout.write("\r>>> Ratings processsed: %i" % count)
		#sys.stdout.flush()

		ln2 = ln.split(",")
		movie = ln2[0]
		avg_rating = float(ln2[1])
		rating_supp = ln2[2].strip()

		if avg_rating >= min_avg_rating:
			for row in movies:
				row = row.split(",", 1)
				if movie == row[0]:
					movie_title_genre = row[1]
					with open("../data/output/a7-movies-extract-recommended-films.csv", "a") as f:
						f.write(ln.strip() + ',' + movie_title_genre)

	print ("\nDone fun7\n")


if __name__ == '__main__':
	fun1("../data/input/v1-input-ratings.csv")
	#"""
	fun2()
	fun3(2, 90)
	fun4()
	fun5()
	fun6()
	fun7()
	#"""


	# parser = argparse.ArgumentParser()
	# parser.add_argument('data_input', help='')
	# args = parser.parse_args()
	# process_images(args.data_input)


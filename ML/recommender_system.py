import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import MySQLdb
import math
import os

db=MySQLdb.connect("localhost","root","root1234","fashion")

label_dict = {
    "red" : 1,
    "black" : 2,
    "shirt" : 3,
    "dress" : 4,
    "orange" : 5,
    "blue" : 6,
    "jeans" : 7,
    "floral" : 8,
    "graphic" : 9,
    "solid" : 10,
    "plaid" : 11,
    "spotted" : 12,
    "striped" : 13
}

MATRIX_SIZE = (NUM_USERS, NUM_APPAREL) = (4, 7)

def executeQuery(query):
	cur = db.cursor()
	cur.execute(query)
	return cur.fetchall()

def insertQuery(query):
	cur = db.cursor()
	cur.execute(query)
	db.commit()

# apparel_list = ['Shirt', 'Pant', 'Watch', 'Shorts', 'Jacket']
# df = pd.DataFrame(np.random.randint(0, 5, size = MATRIX_SIZE), columns=apparel_list, rows=list('ABCDE'))
# data = pd.DataFrame(np.random.randint(0, 5, size = MATRIX_SIZE), columns=apparel_list, rows=list('ABCDE'))

# dummy_data = [[1, 0, 3, 0, 0, 5, 0, 0, 5, 0, 4, 0],
#               [0, 0, 5, 4, 0, 0, 4, 0, 0, 2, 1, 3],
#               [2, 4, 0, 1, 2, 0, 3, 0, 4, 3, 5, 0],
#               [0, 2, 4, 0, 5, 0, 0, 4, 0, 0, 2, 0],
#               [0, 0, 4, 3, 4, 2, 0, 0, 0, 0, 2, 5],
#               [1, 0, 3, 0, 3, 0, 0, 2, 0, 0, 4, 0]
#               ]

def calculate_sigmoid(x):
	return 1/(1+math.exp(-x))

def getAllValues(query):
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def adjust_matrix(apparel_id, adjust_value, user_id):
	labels = getAllValues("select label_id from has_labels where apparel_id = %d" % apparel_id)
	labels = [str(x[0]) for x in labels]
	labels = ",".join(labels)
	print("update prefers set rating = rating + %d where user_id = '%s' and label_id in (%s)" % (adjust_value, user_id, labels))
	insertQuery("update prefers set rating = rating + %d where user_id = '%s' and label_id in (%s)" % (adjust_value, user_id, labels))

def get_recommendations(user_id):
	data1 = executeQuery("select * from prefers")
	d = np.zeros(MATRIX_SIZE)
	for row in data1:
		d[row[0]-1][row[1]-1]=row[2]
	dummy_data = d
	df = pd.DataFrame(dummy_data)
	data = np.array(dummy_data)
	pref = [] 
	# To avoid considering zeros as negative ratings
	df = df.replace(0, np.NaN)
	for i in range(NUM_USERS):
		for j in range(NUM_APPAREL):
			df.iloc[i,j] = calculate_sigmoid(df.iloc[i,j])*5
	# Normalize all values to be centered around 0
	df = df.sub(df.mean(axis=1), axis=0)

	df = df.replace(np.NaN, 0)
	print(df)

	cosine_sim_matrix = cosine_similarity(df)
	num_of_recommendations = 2

	# Exclude max index of 1 and take remaining highest indices
	max_indices = np.argsort(cosine_sim_matrix)[:,-num_of_recommendations-1 : -1]
	user_num = user_id - 1
	rating_indices = max_indices[user_num,:]
	rating_values = cosine_sim_matrix[user_num,rating_indices]
	rating_values = np.array([max(0.1,x) for x in rating_values])

	for item_num in range(7):
		# if data[user_num][item_num] == 0.0:
		data_values = data[rating_indices,item_num]
		final_rating = np.matmul(data_values, rating_values.T) / np.sum(rating_values)
		# print("Rating for user %d on unknown item %s is %f" % (user_num, item_num, final_rating))
		pref.append((item_num, final_rating))

	pref = sorted(pref, key=lambda x : x[1])
	pref = pref[-2:]
	recommendations = executeQuery("select img_path from apparel, has_labels where apparel_id = id and label_id in (%d, %d) order by RAND() limit 5" % (pref[0][1], pref[1][1]))
	recommendations = ["/".join(x[0].split(os.path.sep)[-2:]) for x in recommendations]
	return recommendations


def get_image_for_recommendation():
	data = executeQuery("select * from apparel order by RAND() limit 1")[0]
	img_id = data[0]
	img_path = "/".join(data[1].split(os.path.sep)[-2:])
	return img_id, img_path

def lastInsertedId():
    cursor = db.cursor()
    cursor.execute("select LAST_INSERT_ID()")
    return cursor.fetchone()[0]

def add_user_item(img_path, labels):
	insertQuery("insert into apparel values(0, '%s')" % img_path)
	insertId = lastInsertedId()
	for val in labels:
		insertQuery("insert into has_labels values(%d, %d)" % (insertId, label_dict[val[0]]))
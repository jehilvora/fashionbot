import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import MySQLdb
import math

db=MySQLdb.connect("localhost","root","root123","fashionbot")

MATRIX_SIZE = (NUM_USERS, NUM_APPAREL) = (4, 7)

def executeQuery(query):
	cur = db.cursor()
	cur.execute(query)
	return cur.fetchall()


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

data1 = executeQuery("select * from prefers")
d = np.zeros(MATRIX_SIZE)
for row in data1:
	d[row[0]-1][row[1]-1]=row[2]
dummy_data = d
df = pd.DataFrame(dummy_data)
data = np.array(dummy_data)
print(df)
# To avoid considering zeros as negative ratings
df = df.replace(0, np.NaN)

# Normalize all values to be centered around 0
df = df.sub(df.mean(axis=1), axis=0)

df = df.replace(np.NaN, 0)

print(df)
cosine_sim_matrix = cosine_similarity(df)
print(cosine_sim_matrix)
num_of_recommendations = 2

# Exclude max index of 1 and take remaining highest indices
max_indices = np.argsort(cosine_sim_matrix)[:,-num_of_recommendations-1 : -1]
print(max_indices)
user_num = 2
rating_indices = max_indices[user_num,:]
rating_values = cosine_sim_matrix[user_num,rating_indices]
rating_values = np.array([max(0.1,x) for x in rating_values])

for item_num in range(7):
	# if data[user_num][item_num] == 0.0:
	data_values = data[rating_indices,item_num]
	print(data_values)
	print(rating_values)
	final_rating = np.matmul(data_values, rating_values.T) / np.sum(rating_values)
	print("Rating for user %d on unknown item %s is %f" % (user_num, item_num, final_rating))


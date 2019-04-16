import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

MATRIX_SIZE = (NUM_USERS, NUM_APPAREL) = (5, 5)

# apparel_list = ['Shirt', 'Pant', 'Watch', 'Shorts', 'Jacket']
# df = pd.DataFrame(np.random.randint(0, 5, size = MATRIX_SIZE), columns=apparel_list, rows=list('ABCDE'))
# data = pd.DataFrame(np.random.randint(0, 5, size = MATRIX_SIZE), columns=apparel_list, rows=list('ABCDE'))

dummy_data = [[1, 0, 3, 0, 0, 5, 0, 0, 5, 0, 4, 0],
              [0, 0, 5, 4, 0, 0, 4, 0, 0, 2, 1, 3],
              [2, 4, 0, 1, 2, 0, 3, 0, 4, 3, 5, 0],
              [0, 2, 4, 0, 5, 0, 0, 4, 0, 0, 2, 0],
              [0, 0, 4, 3, 4, 2, 0, 0, 0, 0, 2, 5],
              [1, 0, 3, 0, 3, 0, 0, 2, 0, 0, 4, 0]
              ]

df = pd.DataFrame(dummy_data)
data = np.array(dummy_data)

# To avoid considering zeros as negative ratings
df = df.replace(0, np.NaN)

# Normalize all values to be centered around 0
df = df.sub(df.mean(axis=1), axis=0)

df = df.replace(np.NaN, 0)

cosine_sim_matrix = cosine_similarity(df)

num_of_recommendations = 2

# Exclude max index of 1 and take remaining highest indices
max_indices = np.argsort(cosine_sim_matrix)[:,-num_of_recommendations-1 : -1]

user_num = 0
item_num = 4

rating_indices = max_indices[user_num,:]
data_values = data[rating_indices,item_num]
rating_values = cosine_sim_matrix[user_num,rating_indices]

final_rating = np.matmul(data_values, rating_values.T) / np.sum(rating_values)
print("Rating for user %d on unknown item %s is %f" % (user_num, item_num, final_rating))


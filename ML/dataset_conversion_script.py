#Script to convert dataset for vggnet

import scipy.io as sio
import os
from shutil import copy
import math

def createDir(dir_name):
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")

#Change directories appropriately (better to mention absolute paths)
IMG_PATH = '/Users/i506655/Downloads/ClothingAttributeDataset/images'
MAT_PATH = '/Users/i506655/Downloads/ClothingAttributeDataset/labels'
CREATION_PATH = '/Users/i506655/Downloads/keras-multi-label/custom_dataset'

# For non Yes/No Categories
multi_option_labels = {
	'gender' : ['male', 'female'],
	'skin_exposure': ['low', 'high'],
	'sleevelength': ['no-sleeves', 'short-sleeves', 'long-sleeves'],
	'neckline': ['v-shape', 'round', 'other-shape'],
	'category': ['shirt', 'sweater', 't-shirt', 'outerwear', 'suit', 'tank-top', 'dress']
}

num_images = 1856


mat_files = os.listdir(MAT_PATH)

for mat_file in mat_files:

	# Create base directories for dataset
	label_name = mat_file[:-7]

	if label_name in multi_option_labels:
		for multi_name in multi_option_labels[label_name]:
			dir_name = CREATION_PATH + '/' + multi_name
			createDir(dir_name)
	else:
		dir_name = CREATION_PATH + '/' + label_name
		createDir(dir_name)

	# Populating folders with images
	mat_contents = sio.loadmat(MAT_PATH + '/' + mat_file)['GT']

	for i in range(1,num_images + 1):
		img_src = IMG_PATH + '/' + '{:06}'.format(i) + '.jpg'
		img_dest = ""
		if label_name in multi_option_labels and not math.isnan(mat_contents[i - 1][0]) :
			img_dest = CREATION_PATH + '/' + multi_option_labels[label_name][int(mat_contents[i - 1][0] - 1)]
		elif mat_contents[i - 1] == 2:
			img_dest = CREATION_PATH + '/' + label_name
		if img_dest != "":
			copy(img_src, img_dest)
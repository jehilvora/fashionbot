# import the necessary packages
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import json


# load the trained convolutional neural network and the multi-label
# binarizer
MODEL_NAME_COLOR = "ML/color_apparel.model"
LABEL_BIN_COLOR = "ML/color_labels.lb"
MODEL_NAME_PATTERN = "ML/pattern.model"
LABEL_BIN_PATTERN = "ML/pat_labels.lb"
model_color = load_model(MODEL_NAME_COLOR)
mlb_color = pickle.loads(open(LABEL_BIN_COLOR, "rb").read())
model_pattern = load_model(MODEL_NAME_PATTERN)
mlb_pattern = pickle.loads(open(LABEL_BIN_PATTERN, "rb").read())
graph = tf.get_default_graph() 

def giveLabelPredictions(image, classify_model):
	# load the image
	image = cv2.imread(image)
	output = imutils.resize(image, width=400)
	predictions = {}
	
	# pre-process the image for classification
	image = cv2.resize(image, (96, 96))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# classify the input image then find the indexes of the two class
	# labels with the *largest* probability
	print("[INFO] classifying image...")
	global graph
	proba = None
	with graph.as_default():
		model = model_color if classify_model == "color" else model_pattern
		mlb = mlb_color if classify_model == "color" else mlb_pattern
		proba = model.predict(image)[0]
		idxs = np.argsort(proba)[::-1][:5]

		# show the probabilities for each of the individual labels
		for (label, p) in zip(mlb.classes_, proba):
			predictions[label] = "{:.2f}%".format(p * 100)
			
		return predictions
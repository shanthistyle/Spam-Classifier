from __future__ import division
__author__ = 'ShanthiS'

import numpy
import csv

from numpy import *	
from scipy import stats

# Load data from csv
filename = "../digitsDataset/trainFeatures.csv"
training_features = numpy.loadtxt(filename, delimiter=',')

filename = "../digitsDataset/trainLabels.csv"
training_labels = numpy.loadtxt(filename, delimiter=',')

filename = "../digitsDataset/valFeatures.csv"
val_features = numpy.loadtxt(filename, delimiter=',')

filename = "../digitsDataset/valLabels.csv"
val_labels = numpy.loadtxt(filename, delimiter=',')

filename = "../digitsDataset/testFeatures.csv"
test_features = numpy.loadtxt(filename, delimiter=',')

#for each feature vector in val_features, compute distance between each feature vector in training_features  
def kNearestNeighbors(k, num, to_classify):
	final_classifications = []
	for item1 in to_classify:
		row_num = 0
		distances = []
		sorted_indeces = []
		k_index = []
		if row_num < (num):
			for i in range(0, num):
				item2 = training_features[i]
				c = item2 - item1
				dist = numpy.sqrt(numpy.sum(c**2))
				#dist = numpy.linalg.norm(item2 - item1, axis=1)
				#dist = numpy.apply_along_axis(numpy.linalg.norm, 1, c)
				distances.append(dist)
			# find index of k smalled values -- index into training_labels
			sorted_indeces = numpy.argsort(distances)
			k_index = sorted_indeces[:k]

			# find corresponding training_labels
			candidates = []
			for index in k_index:
				candidates.append(training_labels[index])

			# choose mode (breaking ties)
			frequency = stats.itemfreq(candidates)
			# frequency takes form of [[val1, count], [val2, count]..]
			counts = []
			for item in frequency:
				counts.append(item[1])
			#use argmax to find value that has highest count, if multiple options with same highest count, return first occurence (arbitrary tie break)
			final_classifications.append(candidates[numpy.argmax(counts)])
		else:
			break
		row_num += 1
	#write final_classifications to a csv file == digitsOutputk.csv
	to_print = numpy.array(final_classifications).astype(int)
	filename = "digitsOutput" + str(k) + ".csv"
	numpy.savetxt(filename, to_print, fmt='%i', delimiter=',')
	return final_classifications

	#print("=== FINAL ====")
	#print(final_classifications)


def errorRate(k, num):
	# Calculate error rate
	# for each classifiation, set to 1 if right --- [actual (1000) - ours (sum of all 1)]/ actual (1000)
	final_classifications = kNearestNeighbors(k, num, val_features)
	num_correct = 0
	i = 0
	for item in final_classifications:
		if (item == val_labels[i]):
			num_correct += 1
		i += 1
	actual = len(final_classifications)
	error_rate = ((actual - num_correct)/actual)*100
	return error_rate

def experimentWithKVals(trial_k):
	for k in trial_k:
		error_rate = errorRate(k, 6000)
		print("error rate for k = " + str(k) + " is " + str(error_rate) + " %")

# === MAIN ===

experimentWithKVals([1, 2, 5, 10, 25])


#write test_classifications to a file
test_classifications = kNearestNeighbors(1, 6000, test_features)
to_print = numpy.array(test_classifications).astype(int)
numpy.savetxt('digitsOutput.csv', to_print, fmt='%i', delimiter=',') #prints as floats








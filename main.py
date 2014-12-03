import csv
import math
import random
import collections

def main(T):
	forest = {}
	data = getData()
	features = data['features']
	labels = [(data['labels'][i], features[i]) for i in range(len(features))]

	while(count < T):
		labelSubset = getSubset(labels)
		count+=1
	
def getSubset(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])
	result = []
	n = len(labels)

	for i in range(len(labels)):
		result.push(labels[random.randint(0, n-1)])
	return result
def getData():
	result = {'features': [], 'labels': []}

	with open('trainFeatures.csv', 'rb') as csvfile:
		features = csv.reader(csvfile, delimiter='\n')
	    result['features'] = [row.split(',') for row in features]

   	with open('trainLabels.csv', 'rb') as csvfile:
   		result['labels'] = csv.reader(csvfile, delimiter='\n')

	return result


def Tree():
	return collections.defaultdict(Tree)

def buildDecTree(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])

	same = true
	stopCondition = len(labels[0][1]) == 1
	t = Tree()

	for j in range(len(labels)):
		if labels[j] != labels[i]:
			same = false
			break;

	if same or stopCondition:
		t[1] = {'value': {'fIndex':null, 'fThreshold': labels[0][0]}}
		return t


	featuresLen = len(labels[0][1])
	possibleIndices = [i for i in range(featuresLen) if labels[0][1][i] != -1]

	if featuresLen > 8:
		featureSubset = sorted(random.sample(possibleIndices, 8))
	else:
		featureSubset = possibleIndices

	maxGain = 0
	maxThreshold = thresholds[0]
	maxFeatureI = 0


	for j in featureSubset:
		currF = sorted(set([labels[i][1][j] for i in range(len(labels))])) # values of random feature for len(labels) emails
		thresholds = [(currF[i] + currF[i+1])/2 for i in range(len(currF) - 1)]
		

		for k in range(len(thresholds)):
			t = thresholds[k]
			temp = max(maxGain, computeGain(labels, t, j))
			if temp != maxGain:
				maxGain, maxThreshold, maxFeatureIndex = temp, t, j

	leftList, rightList = [], []

	for j in range(len(labels)):
		if labels[j][1][maxFeatureIndex] <= maxThreshold:
			temp = labels[j]
			temp[1][maxFeatureIndex] = -1
			leftList.push(temp)
		else:
			temp = labels[j]
			temp[1][maxFeatureIndex] = -1
			rightList.push(temp)

	left = buildDecTree(leftList)
	right = buildDecTree(rightList)

	t[1] = {'value': {'fIndex':maxFeatureIndex, 'fThreshold': maxThreshold}}
	print(t[1])
	t[2][1] = left
	t[2][2] = right
	return t

def computeGain(labels, t, featureIndex):
	left, right = [], []

	for i in range(len(labels)):
		if labels[i][1][featureIndex] <= t:
			left.push((labels[i][0], labels[i][1]))
		else:
			right.push((labels[i], featureVals[i]))

	probList = [(labels[i][0], labels[i][1][featureIndex]) for i in range(len(labels))]

	ent = entropy(probList)
	entL = entropy(left)
	entR = entropy(right)

	print(ent)
	print("\t" + entL)
	print("\t" + entR)
	print("\n\n")

	return (ent - (len(left)/len(labels))*entL + (len(right)/len(labels))*entR

	

def entropy(probList):
	#probList = tuples of (label, featureVal) for a given feature

	if len(probList == 0):
		return 0

	summation = []

	for elem in range(len(probList))):
		if elem[0] == 1:
			P = elem[1]
			summation.push(P * math.log(P, 2))
		else:
			summation.push(0)

	return 0 - sum(summation)







import csv
import math
import random
import collections

def main(T):
	forest = {}
	data = getData()
	features = data['features']
	labels = [(data['labels'][i], features[i]) for i in range(len(features))]
	count = 0
	featureIndices = []

	while(count < T):
		labelSubset = getSubset(labels)
		tree = buildDecTree(labelSubset)
		featureIndices.append(tree[1])
		print(tree[1])
		count+=1

	print(featureIndices)
	
def getSubset(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])
	result = []
	n = len(labels)

	for i in range(len(labels)):
		result.append(labels[random.randint(0, n-1)])
	return result

def getData():
	result = {'features': [], 'labels': []}

	with open('emailDataset/trainFeatures.csv', 'rb') as csvfile:
		features = csv.reader(csvfile, delimiter=',')
		result['features'] = [[float(r) for r in row] for row in features]

   	with open('emailDataset/trainLabels.csv', 'rb') as csvfile:
   		labels = csv.reader(csvfile, delimiter=' ')
   		result['labels'] = [int(row[0]) for row in labels]

	return result


def Tree():
	return collections.defaultdict(Tree)

def buildDecTree(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])

	same = True
	stopCondition = len(labels[0][1]) == 1
	t = Tree()

	for j in range(len(labels)):
		if labels[0][0] != labels[j][0]:
			same = False
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
	maxThreshold = 0
	maxFeatureIndex = 0


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
			leftList.append(temp)
		else:
			temp = labels[j]
			temp[1][maxFeatureIndex] = -1
			rightList.append(temp)

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
			left.append((labels[i][0], labels[i][1][featureIndex]))
		else:
			right.append((labels[i][0], labels[i][1][featureIndex]))

	probList = [(labels[i][0], labels[i][1][featureIndex]) for i in range(len(labels))]

	ent = entropyCalc(probList)
	entL = entropyCalc(left)
	entR = entropyCalc(right)

	return ent - (len(left)/len(labels))*entL + (len(right)/len(labels))*entR

	

def entropyCalc(probList):
	#probList = tuples of (label, featureVal) for a given feature

	if len(probList) == 0:
		return 0

	summation = []

	for elem in probList:
		if elem[0] == 1:
			P = elem[1]
			if (P > 0):
				summation.append(P * math.log(P, 2))
			else: 
				summation.append(0)
		else:
			summation.append(0)

	return 0 - sum(summation)



main(1)



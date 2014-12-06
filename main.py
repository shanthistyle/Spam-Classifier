import csv
from Tree import Tree
import math
import random

def main(T):
	forest = {}
	trainData = getTrainingData()
	trainFeatures = trainData['features']
	trainLabels = [(trainData['labels'][i], trainFeatures[i]) for i in range(len(trainFeatures))]
	trainingTrees = []
	count = 0

	while(count < T):
		labelSubset = getSubset(trainLabels)
		tree = buildDecTree(labelSubset)
		trainingTrees.append(tree)
		count+=1

	# valData = getValData()
	# valFeatures = valData['features']
	# valLabels = [(valData['labels'][i], valFeatures[i]) for i in range(len(valFeatures))]
	testData = getTestData()
	testFeatres = testData['features']
	countCorrect = 0
	for i in range(len(valLabels)):
		
		label = valLabels[i][0]
		resultList = []

		for tree in trainingTrees:
			temp = computeResult(tree, valLabels[i][1])
			resultList.append(temp)

		if (len([x for x in resultList if x == 1]) >= len(resultList)/2):
			if (label == 1):
				countCorrect+=1
		elif label == 0:
			countCorrect+=1

	print(str((float(countCorrect)/len(valLabels))))
def getTestData():
	result = {'features': [], 'labels': []}

	with open('emailDataset/testFeatures.csv', 'rb') as csvfile:
		features = csv.reader(csvfile, delimiter=',')
		result['features'] = [[float(r) for r in row] for row in features]

   	return result

def computeResult(tree, features):
	while tree.left and tree.right:
		if (features[tree.featureIndex] > tree.threshold):
			# print("Feature: " + str(tree.featureIndex) + " > " + str(tree.threshold))
			if tree.right:
				tree = tree.right
			else:
				return tree.verdict
		else:
			# print("Feature: " + str(tree.featureIndex) + " <= " + str(tree.threshold))
			if tree.left:
				tree = tree.left
			else:
				return tree.verdict

	return tree.verdict
def getSubset(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])
	result = []
	n = len(labels)

	for i in range(len(labels)):
		result.append(labels[random.randint(0, n-1)])
	return result

def getTrainingData():
	result = {'features': [], 'labels': []}

	with open('emailDataset/trainFeatures.csv', 'rb') as csvfile:
		features = csv.reader(csvfile, delimiter=',')
		result['features'] = [[float(r) for r in row] for row in features]

   	with open('emailDataset/trainLabels.csv', 'rb') as csvfile:
   		labels = csv.reader(csvfile, delimiter=' ')
   		result['labels'] = [int(row[0]) for row in labels]

	return result

def getValData():
	result = {'features': [], 'labels': []}

	with open('emailDataset/valFeatures.csv', 'rb') as csvfile:
		features = csv.reader(csvfile, delimiter=',')
		result['features'] = [[float(r) for r in row] for row in features]

   	with open('emailDataset/valLabels.csv', 'rb') as csvfile:
   		labels = csv.reader(csvfile, delimiter=' ')
   		result['labels'] = [int(row[0]) for row in labels]

   	return result

def buildDecTree(labels):
	# labels = list of tuples: (labelVal = 0 or 1, [featureVals])

	same = True
	stopCondition = len(labels) == 0 or len(labels[0][1]) == 1
	t = Tree()

	for j in range(len(labels)):
		if labels[0][0] != labels[j][0]:
			same = False
			break;

	if same or stopCondition:
		t.right = None
		t.left = None
		t.featureIndex = None
		t.threshold = None
		if len(labels) > 0:
			t.verdict = labels[0][0]
		else:
			t.verdict = 1

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
		# currF = values of random feature for len(labels) emails
		currF = sorted(set([labels[i][1][j] for i in range(len(labels)) if labels[i][1][j] != -1])) 
		thresholds = [(currF[i] + currF[i+1])/2 for i in range(len(currF) - 1)]

		for k in range(len(thresholds)):
			t = thresholds[k]
			temp = max(maxGain, computeGain(labels, t, j))
			if temp != maxGain:
				maxGain, maxThreshold, maxFeatureIndex = temp, t, j

	leftList, rightList = [], []

	for j in range(len(labels)):
		if labels[j][1][maxFeatureIndex] != -1 and labels[j][1][maxFeatureIndex] <= maxThreshold:
			temp = labels[j]
			temp[1][maxFeatureIndex] = -1
			leftList.append(temp)
		elif labels[j][1][maxFeatureIndex] != -1:
			temp = labels[j]
			temp[1][maxFeatureIndex] = -1
			rightList.append(temp)

	t = Tree()
	t.featureIndex = maxFeatureIndex
	t.threshold = maxThreshold
	# print(str(t.featureIndex) + " <= " + str(t.threshold))
	if len(leftList) > 0 and len(rightList) > 0:
		left = buildDecTree(leftList)
		right = buildDecTree(rightList)
		t.left = left
		t.right = right

	elif len(leftList) > 0:
		temp = Tree()
		temp.verdict = leftList[0][0]
		temp2 = Tree()

		if leftList[0][0]:
			temp2.verdict = 0
		else: 
			temp2.verdict = 1


		t.left = buildDecTree(leftList)
		t.right = temp2
	elif len(rightList) > 0:
		temp = Tree()
		temp.verdict = rightList[0][0]
		temp2 = Tree()

		if rightList[0][0]:
			temp2.verdict = 0
		else: 
			temp2.verdict = 1


		t.left = temp2
		t.right = buildDecTree(rightList)
	else:
		count = len([elem[0] for elem in labels if elem[0] == 1])
		if float(count)/len(labels) > .5:
			t.verdict = 1
		else:
			t.verdict = 0
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
	entR = entropyCalc(right)
	entL = entropyCalc(left)

	return ent - ((len(left)/len(labels))*entL + (len(right)/len(labels))*entR)

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



main(2)



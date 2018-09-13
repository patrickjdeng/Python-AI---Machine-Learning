# Patrick Deng
# CS 4375.501
# ID3
# Inputs: file of training instances, file of testing instances, max number of training instances
# Outputs: the produced decision tree, as well as its training and testing accuracies
# The tree is produced through the ID3 algorithm given the attributes and class of each instance
# The tree is stored via a binary tree, represented as arrays which link to zero or two other arrays

import math
import sys

CHOICE = 0
LEFT = 1
RIGHT = 2
ISLEAF = 3

def main():
    trainingInputs = readTrainingSet()
    # don't count the class as atribute
    attributes = trainingInputs[0]
    trainingSet = trainingInputs[1]
    tree = buildTree(-1, -1, attributes, trainingSet,trainingSet)
    print(getTreeString(tree, 0))
    testSet = readTestSet()
    testTree(tree,trainingSet,testSet, attributes)


def readTrainingSet():
    attributes = []
    instances = []
    file = open(sys.argv[1])

    trainingSize = 0
    maxtrainingSize = int(sys.argv[3])

    for line in file:
        line = line.strip('\n')
        if ' ' in line:
            continue
        elif len(line) == 0:
            continue
        elif trainingSize == 0:
            attributes = line.split('\t')
            trainingSize += 1
        elif trainingSize < \
                maxtrainingSize + 1:
            line = line.split('\t')
            line = list(map(int, line))
            instances.append(line)
            trainingSize += 1
        else:
            break

    inputs = [attributes, instances]
    return inputs


def readTestSet():
    inputs = []
    file = open(sys.argv[2])
    firstLine = True
    for line in file:
        line = line.strip('\n')
        if ' ' in line:
            continue
        elif len(line) == 0:
            continue
        elif firstLine:
            firstLine = False
        else:
            inputs.append(line.split('\t'))
    return inputs


def count(value, attributeIndex, set):
    count = 0
    for instance in set:
        if instance[attributeIndex] == value:
            count += 1
    return count

# takes in set to consider and index of attribute to calculate IG around
def calculateIG(trainingSet, PICKED):
    attrTrueCount = 0
    attrFalseCount = 0
    CLASS = len(trainingSet[0]) - 1

    # calculate parent entropy
    total = len(trainingSet)
    classCountYes = count(1, CLASS, trainingSet)
    classCountNo = count(0, CLASS, trainingSet)
    parentEntropy = -1 * classCountYes / total * math.log(classCountYes / total, 2) + -1*classCountNo/total* math.log(classCountNo/ total, 2)

    # sort into left and right by the picked field
    leftSet = []
    rightSet = []
    for i in range(len(trainingSet)):
        if trainingSet[i][PICKED] == 0:
            leftSet.append(trainingSet[i])
        else:
            rightSet.append(trainingSet[i])

    # calculate left entropy
    leftSize = len(leftSet)
    leftClassYes = count(1, CLASS, leftSet)
    leftClassNo = count(0, CLASS, leftSet)
    if leftClassYes == 0:
        leftEntropyYes = 0
    else:
        leftEntropyYes = -1 * leftClassYes / leftSize * math.log(leftClassYes / leftSize, 2)
    if leftClassNo == 0:
        leftEntropyNo = 0
    else:
        leftEntropyNo = -1 * leftClassNo / leftSize * math.log(leftClassNo / leftSize, 2)

    #right entropy
    rightSize = len(rightSet)
    rightClassYes = count(1, CLASS, rightSet)
    rightClassNo = count(0, CLASS, rightSet)
    if rightClassYes == 0:
        rightEntropyYes = 0
    else:
        rightEntropyYes = -1 * rightClassYes / rightSize * math.log(rightClassYes / rightSize, 2)
    if rightClassNo == 0:
        rightEntropyNo = 0
    else:
        rightEntropyNo = -1 * rightClassNo / rightSize * math.log(rightClassNo / rightSize, 2)
    probLeft = len(leftSet) / len(trainingSet)
    probRight = len(rightSet) / len(trainingSet)


    entropyLeft = leftEntropyNo + leftEntropyYes
    entropyRight = rightEntropyNo + rightEntropyYes
    return parentEntropy - (probLeft * entropyLeft + probRight * entropyRight)


# recursive algorithm to build binary tree
def buildTree(selectedAttribute, selectedValue, attributes, trainingSet, fullSet):
    root = []
    CLASS = len(attributes) - 1

    # choice from previous node
    if selectedAttribute != -1:
        root.append(selectedAttribute + " = " + str(selectedValue) + " : ")
    else:
        root.append("")

    #attach left and right nodes
    root.append([])
    root.append([])
    root.append(True)

    # count number of class positives *and negatives*
    # check if pure
    classCountYes = count(1, CLASS, trainingSet)
    total = len(trainingSet)

    if total == 0:
        return root
    # if pure
    elif classCountYes/total == 0 or classCountYes/total == 1:
        if classCountYes / total == 0:
            root[CHOICE] += " 0"
        else:
            root[CHOICE] += " 1"
    #if impure and no attributes
    elif len(attributes) <= 1:
        #return most valued in set
        if count(1, CLASS, trainingSet) < count(0,CLASS, trainingSet):
            root[CHOICE] += "0"
        elif count(1, CLASS, trainingSet) < count(0,CLASS, trainingSet):
            root[CHOICE] += "1"
        else:
            if count(1, CLASS, fullSet) < count(0, CLASS, fullSet):
                root[CHOICE] += " 0"
            elif count(1, CLASS, fullSet) < count(0, CLASS, fullSet):
                root[CHOICE] += "1"
    # if impure and attributes left
    else:
        root[ISLEAF] = False

        PICKED = 0
        # calculate IG
        igs = []
        for i in range(len(attributes)-1):
            igs.append(calculateIG(trainingSet, i))

        # pick the first maximum
        PICKED = igs.index(max(igs))

        # remove current attribute from left and right attr sets
        childAttributes = []

        for i in range(len(attributes)):
            if i != PICKED:
                childAttributes.append(attributes[i])

        # prepare left and right node instance sets
        childTrainingSet = []; leftSet = []; rightSet = []

        # remove current field from left and right test sets
        for instance in trainingSet:
            childInstance = []
            for i in range(len(instance)):
                if i != PICKED:
                    childInstance.append(instance[i])
            childTrainingSet.append(childInstance)

        # sort into left and right by the picked field
        for i in range(len(trainingSet)):
            if trainingSet[i][PICKED] == 0:
                leftSet.append(childTrainingSet[i])
            else:
                rightSet.append(childTrainingSet[i])
        # left
        root[LEFT] = buildTree(attributes[PICKED], 0, childAttributes, leftSet, fullSet)
        # right
        root[RIGHT] = buildTree(attributes[PICKED], 1, childAttributes, rightSet, fullSet)


    return root


def getTreeString(root, level):
    treeString = ""
    if root[LEFT] != [] or root[RIGHT] != []:
        for i in range(level-1):
            treeString += "|\t"
        treeString += root[CHOICE] + '\n'
        treeString += getTreeString(root[LEFT],level + 1)
        treeString += getTreeString(root[RIGHT], level + 1)
    else:
        for i in range(level-1):
            treeString += "|\t"
        treeString += root[CHOICE] + '\n'
    return treeString

def testTree(tree, trainingSet, testSet, attributes):
    CLASS = len(testSet[0]) - 1
    trainingSize = int(sys.argv[3])

    trainCount = 0
    for instance in trainingSet:
        if str(testInstance(instance,tree,attributes)) == str(instance[CLASS]):
            trainCount += 1
    trainAccuracy = trainCount/trainingSize

    testCount = 0
    for instance in testSet:
        if str(testInstance(instance,tree,attributes)) == str(instance[CLASS]):
            testCount += 1
    testAccuracy = testCount/len(testSet)
    print("Accuracy on training set (" + str(trainingSize) + " instances): " + str(trainAccuracy*100) + "%")
    print("Accuracy on test set (" + str(len(testSet)) + " instances): " + str(testAccuracy*100) + "%")

#returns a value 0 or 1
def testInstance(instance, root, attributes):
    #if at leaf
    line = root[CHOICE].split(" ") #attribute, = , selectvalue, : , class value
    if root[ISLEAF] == True:
        return line[-1]
    # if not at leaf
    else:
        nextline = root[LEFT][CHOICE].split(" ")  # attribute, = , selectvalue, : , class value
        if instance[attributes.index(nextline[0])] == 0:
            return testInstance(instance,root[LEFT],attributes)
        else:
            return testInstance(instance,root[RIGHT],attributes)

main()

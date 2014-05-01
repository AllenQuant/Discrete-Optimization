#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from numpy import zeros
from copy import deepcopy

class Item:
    def __init__(self, value, weight, position=0, score=0):
        self.value = value
        self.weight = weight
        self.position = position
        self.score = 0
        self.chocolate = float(self.value)/float(self.weight)

    def add_value(self, value):
        self.value += value

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class BbItem:

    def __init__(self, value, maxEstimate, list=None):
        self.value = value
        self.maxEstimate = maxEstimate
        if list == None:
            self.list = []
        else:
            self.list = list

    def add_value(self, value):
        return BbItem(self.value + value, self.maxEstimate, self.list)


    # def withItem(self):
    #     return BbItem(self.value, self.score, self.list + [1])

    def withoutItem(self):
        return BbItem(self.value, self.maxEstimate, self.list + [0])

    def addToList(self, position):
        self.list.append(position)

    def withItem(self, position):
        return BbItem(self.value, self.maxEstimate, self.list + [position])

    def orderedList(self, count):
        xx = zeros(count, int)
        xx[self.list] = 1
        return xx.tolist()




def solve_it(inputData):
    t0 = time.time()
    # Modify this code to run your optimization algorithm

    #value, taken = withDynamicProgramming(inputData)
    # value, taken = withBranchAndBound(inputData)
    value, taken = withIterativeBranchAndBound(inputData)

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))

    print time.time() - t0, "seconds process time"

    return outputData

def solve_it2(inputData):
    print "solveIt2"
    t0 = time.time()
    # Modify this code to run your optimization algorithm

    #value, taken = withDynamicProgramming(inputData)
    value, taken = withBranchAndBound(inputData)
    # value, taken = withIterativeBranchAndBound(inputData)

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))

    print time.time() - t0, "seconds process time"

    return outputData

def withDynamicProgramming(inputData):
    heap, capacity = create_list(inputData)
    value, taken = dynamicProgramming(heap, capacity)
    return value, taken

def withBranchAndBound(inputData):
    list, capacity, estimate =  create_sorted_list(inputData)
    return BranchAndBound(list, capacity, estimate)

def withIterativeBranchAndBound(inputData):
    list, capacity, estimate =  create_sorted_list(inputData)
    return IterativeBranchAndBound(list, capacity, estimate)


def create_list(inputData):
    # parse the input
    lines = inputData.split('\n')

    capacity = int(lines[0].split()[1])

    items = []
    maxValue = 0

    for i in range(1, len(lines) - 1):
        line = lines[i].split()

        item = Item(int(line[0]), int(line[1]))
        maxValue += item.value
        items.append(item)

    return items, capacity


def create_sorted_list(inputData):
    # parse the input
    lines = inputData.split('\n')

    capacity = int(lines[0].split()[1])

    items = []

    for i in range(1, len(lines) - 1):
        if len(lines[i].strip()) > 0:
            line = lines[i].split()

            item = Item(int(line[0]), int(line[1]), i - 1)
            items.append(item)

    estimate = estimator(items, 0, capacity)
    items.sort(key=lambda item: item.chocolate, reverse=True)
    return items, capacity, estimate

def dynamicProgramming(items, capacity, list=[]):
    if len(items) == 0:
        return 0, list

    withoutItem = dynamicProgramming(items[1:], capacity, list + [0])
    if items[0].weight <= capacity:
        withItem = dynamicProgramming(items[1:], capacity - items[0].weight,  list + [1])
        withItem = withItem[0] + items[0].value, withItem[1]
        if withItem[0] > withoutItem[0]:
            return withItem
    return withoutItem

maxScore = BbItem(0, 0)

def BranchAndBound(items, capacity, estimate):
    print "capacity =", capacity, "Estimate =", estimate
    BranchAndBoundAcc(items, len(items), 0, capacity, BbItem(0, estimate), estimate)
    return maxScore.value, maxScore.orderedList(len(items))


def BranchAndBoundAcc(items, size, it, capacity, bbItem, maxEstimate):
    global maxScore

    if size == it or capacity == 0 or maxEstimate < maxScore.value:
        if bbItem.value > maxScore.value:
            maxScore = bbItem
        return
    item = items[it]

    if item.weight <= capacity:
        BranchAndBoundAcc(items, size, it + 1, capacity - item.weight, bbItem.add_value(item.value).withItem(item.position), maxEstimate)

    estimate = estimator(items, it + 1, capacity)
    BranchAndBoundAcc(items, size, it + 1, capacity, bbItem, estimate + bbItem.value)

    return


def IterativeBranchAndBound(items, capacity, estimate):
    maxItem = BbItem(0, 0)

    stack = []
    endList = len(items) - 1
    currentCapacity = capacity

    stack.append((0, False, capacity, BbItem(0, estimate)))
    stack.append((0, True, capacity, BbItem(0, estimate)))

    while(len(stack) > 0):
        it, withItem, currentCapacity, currentItem = stack.pop()

        if withItem:
            if items[it].weight <= currentCapacity:
                currentCapacity -= items[it].weight
                currentItem.value += items[it].value
                currentItem.addToList(items[it].position)
            else:
                continue
        else:
            currentItem.maxEstimate = estimator(items, it+1, currentCapacity) + currentItem.value

        #if currentItem.maxEstimate < maxItem.value:
        #    continue

        if currentCapacity == 0 or currentItem.maxEstimate < maxItem.value or it == endList:
            if currentItem.value > maxItem.value:
                maxItem = currentItem
            continue

        if it < endList:
            stack.append((it + 1, False, deepcopy(currentCapacity), deepcopy(currentItem)))
            stack.append((it + 1, True, deepcopy(currentCapacity), deepcopy(currentItem)))

    return maxItem.value, maxItem.orderedList(len(items))


def estimator(items, it, capacity):
    estimate = 0
    size = len(items)
    for i in xrange(it, size):
        if items[i].weight >= capacity:
            estimate += capacity * items[i].chocolate
            break
        else:
            estimate += items[i].value
            capacity = capacity - items[i].weight
    return estimate



import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        if len(sys.argv) > 2:
            print solve_it2(inputData)
        else:
            print solve_it(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

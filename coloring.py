#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import itertools
from collections import Counter

def solve_it(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    degree = []
    for i in range(0, nodeCount):
        edges.append([])
        degree.append(0)
    
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()      
        edges[int(parts[0])].append(int(parts[1]));
        edges[int(parts[1])].append(int(parts[0]));
        degree[int(parts[0])] += 1
        degree[int(parts[0])] += 1

    def greedy_coloring(ordering):
        count = 0
        color = [-1] * nodeCount
        
        for item in ordering:
            vis = [0] * (count + 1)
            for x in edges[item]:
                if color[x] != -1:
                    vis[color[x]] = 1
            for i in range(0, count):
                if vis[i] == 0:
                    color[item] = i;
                    break;
            if color[item] == -1:
                color[item] = count;
                count += 1;
        value = 0;
        
        c = Counter(color);
        
        for item in c:
            value+= c[item]**2.5
        value -= len(c)**3
        return (-value,color,count)
        
    def cross(perm1,perm2):
        l = len(perm1)
        vis = [ 0 ]* (l+1)
        cnt = 0
        bound = l/2
        for i in perm1:
            if cnt<bound:
                vis[i]=1
                cnt+=1
        ret = []
        for x in perm2:
            if not vis[x]:
                vis[x]=1
                ret.append(x)
                cnt+=1
            if cnt==l:
                break
        ret += perm1[:bound]
        return ret
    def mutate(perm,num):
        ret = perm[:]
        l = len(perm)
        for i in range(num):
            r1 = random.randint(0,l-1)
            r2 = random.randint(0,l-1)
            t = ret[r1]
            ret[r1]=ret[r2]
            ret[r2]=t
        return ret
        
        
    print 'node#', nodeCount, 'edge#', edgeCount    
    # build a trivial solution
    # every node has its own color
    solution = greedy_coloring(range(0, nodeCount))
    
    order = range(0, nodeCount)
    random.shuffle(order)

    pcnt =100
    population= []

    
    for i in range(pcnt):
        random.shuffle(order)
        population.append((greedy_coloring(order),order[:]))


    val = 1e9
    for i in range(0,100):
        if i%20==0:
            print i
        vl = population[:]
        for v in vl:
            o = v[1]
            o=mutate(o,random.randint(1,5))
            sol = greedy_coloring(o)
            population.append((sol,o))
            if sol[0] < v[0][0]:
                if sol[0]<val:
                    print 'update 1 value from',val,'to',sol[0]
                    val=sol[0]
                if sol[2] < solution[2]:
                    print 'update 1 from',solution[2],'to',sol[2]
                    solution=sol
        for i in range(len(vl)):
            r1 = random.randint(0,pcnt-1)
            r2 = random.randint(0,pcnt-1)
            o = cross(vl[r1][1],vl[r2][1])
            sol = greedy_coloring(o)
            population.append((sol,o))
            if sol[0]<val:
                print 'update 2 value from',val,'to',sol[0]
                val=sol[0]
            if sol[2] < solution[2]:
                print 'update 2 from',solution[2],'to',sol[2]
                solution=sol            
        population.sort()
        population=population[:pcnt]

            

    # prepare the solution in the specified output format
    outputData = str(solution[2]) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution[1]))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solve_it(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

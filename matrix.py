import yaml
import copy
import math
import numpy as np
import os.path

#this file does all kind of matrix operations

#
#data = dict(
#  B = dict(
#    C = 0,
#    D = 0,
#    E = 0,
#  )
#)
globalDataName = "global*"

data = dict()

#load file
def load(filename):
  d = None
  if (os.path.isfile(filename)):    
    with open(filename, 'r') as f:
      d = yaml.load(f)
  if not(d):
    d = dict()
  return d
# save file
def save(filename,data):
  with open(filename,'w') as saveFile:
    yaml.dump(data, saveFile, default_flow_style=False)

#increment value
def increment(pkey,ckey,data):
  temp = data.get(pkey,{})
  temp_value = temp.get(ckey,0)
  temp_value += 1
  temp[ckey] = temp_value
  data[pkey] = temp
  return data


def incrementValue(key,data):
  temp = data.get(key,0)
  temp_value += 1
  data[key] = temp_value
  return data

# insert new pair
def insert(a,b,data):
  
  data = increment(a,b,data) 
  data = increment(b,a,data)
  return data 

# not working as intended when inserting a triple
def insertTriple(a,b,c,data):
  subdataA = data.get(a,{})
  subdataB = data.get(b,{})
  subdataC = data.get(c,{})
  globaldata = data.get(globalDataName,{})
  subdataA = increment(b,c,subdataA) 
  subdataB = increment(a,c,subdataB)
  subdataC = increment(a,b,subdataC)

  globaldata = increment(a,b,globaldata)
  globaldata = increment(b,a,globaldata)
  globaldata = increment(b,c,globaldata)
  globaldata = increment(c,b,globaldata)
  globaldata = increment(a,c,globaldata)
  globaldata = increment(c,a,globaldata)
  data[a] = subdataA
  data[b] = subdataB
  data[c] = subdataC
  data[globalDataName] = globaldata
  return data 

def getKeyDBIndex(data):
  keyDBIndex = dict()
  indexDBKey = dict()
  #keys = [key for key in data.keys() if key != globalDataName ] 
  keys = data.keys()
  for id, key in enumerate(keys):
    keyDBIndex[key] = id
    indexDBKey[id] = key
  return (keyDBIndex,indexDBKey)

def getMatrix(data,indexDB):
  # get a Matrix indexDB x indexDB
  length = len(indexDB.keys())
  print("length",length)
  vector = [0]*length
  matrix = [vector]*length
  matrix = []
  for i in range(length):
    selectedDB = data.get(indexDB[i],{})
    row = []
    for j in range(length):
      value = selectedDB.get(indexDB[j],0)
      row.append(value)
    matrix.append(row)  
  return matrix

def matrixDelRow(matrix,index):
  tempMatrix = copy.deepcopy(matrix)
  #print(tempMatrix)
  if index < len(tempMatrix):
    tempMatrix.pop(index)
  return tempMatrix

def matrixDelCol(matrix,index):
  tempMatrix = copy.deepcopy(matrix)
  if len(tempMatrix) > 0 and index < tempMatrix[0]:
    for row in tempMatrix:
      row.pop(index)
  return tempMatrix

def matrixGetCol(matrix,index):
  tempCol = []
  if len(matrix) > 0 and index < len(matrix[0]):
    for row in matrix:
      tempCol.append(row[index])
  return tempCol
 
def matrixReplaceCol(matrix,index,col):
  tempMatrix = copy.deepcopy(matrix)
  if len(col) == len(tempMatrix)   and index < len(tempMatrix[0]):
    for row,value in zip(tempMatrix,col):
      row[index] = value
  return tempMatrix

def normaliseList(rawList,accuracy=4):
  total = float(sum(rawList))
  denominator = len(rawList)
  denominator = denominator if denominator > 0 else 0.01
  mean = total/denominator
  # calculate standard deviation
  std = math.sqrt(sum( [pow((x - mean),2) for x in rawList] ) / (denominator - 1))
  normalisedList = [ round((x - mean)/std,accuracy) for x in rawList ]
  return normalisedList

def normaliseMatrix(matrix):
  tempMatrix = copy.deepcopy(matrix)
  colNum = 0
  if len(tempMatrix) > 0 and len(tempMatrix[0]):
    colNum = len(tempMatrix[0])
  for i in range(colNum):
    col = matrixGetCol(tempMatrix,i)
    normalisedCol = normaliseList(col)
    tempMatrix = matrixReplaceCol(tempMatrix,i,normalisedCol)
  return tempMatrix
  
if __name__=="__main__":
  filename = "data.yaml"
  save("data.yaml",data)
  d = load(filename)
  print(d)
  d = insert("D","C",d)
  d = insert("B","C",d)
  d = insert("D","C",d)
  print(d)
  #globalMatrix = d[globalDataName]
  #keyDB,indexDB = getKeyDBIndex(globalMatrix)
  #print(keyDB)
  #matrix = getMatrix(globalMatrix,indexDB)
  #print(matrix)
  keyDB,indexDB = getKeyDBIndex(d)
  print(keyDB)
  matrix = getMatrix(d,indexDB)
  print(matrix)
  #print("pop row",matrixDelRow(matrix,2))
  #print("pop col",matrixDelCol(matrix,2))
  #print(matrix)
  col = matrixGetCol(matrix,2)
  print(col)
  col[0] = 3
  print(col)
  print(matrix)
  print("replaced",matrixReplaceCol(matrix,2,[0,0,1]))
  print(matrix)
  print(normaliseList([1,2,3,4,5]))
  print(matrix)
  print(normaliseMatrix(matrix))
  save("data.yaml",matrix)

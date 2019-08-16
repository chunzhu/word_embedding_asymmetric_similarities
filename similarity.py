import numpy as np
import pandas as pd
import matrix
import argparse

# instruction lists
# convert words to vec
# python testGenSimMatrix.py 
# create a similarity cache list
# python similarity.py --buildcache True 
# convert cache list to one to one list
# python similarityCache.py

parser = argparse.ArgumentParser(description="similarity")
parser.add_argument('--buildcache', help="specify document name",action='store_true', default=False)
parser.add_argument('--crawl', help="specify document name",action='store_true', default=False)
args = parser.parse_args()
buildcache = args.buildcache
crawl = args.crawl

# https://2oxmwwwph5co7td12vvg9v11-wpengine.netdna-ssl.com/wp-content/uploads/2018/04/Reasoning-by-Cognitive-Distance_Final-1.pdf
# https://2oxmwwwph5co7td12vvg9v11-wpengine.netdna-ssl.com/wp-content/uploads/2018/04/Intel-Saffron-Natural-Intelligence_Final.pdf
# use closest neighbour to find words that are close to each other
# if words are close and inversely close to each other, they can be use interchange-ably
# use similarity and disimilarity to reduce redundant information

# calculate the nearest neighbour for all the words in the list

def loadfile(filename):

  f = open(filename,"r")
  return f


def convertFiletoMatrix(f):
  wordToIndex = {}
  wordsVectorList = []
  i = 0

  for index,line in enumerate(f):
    
    line = line.rstrip("\r\n")
    line = line.rstrip("\n")
    line = line.rstrip(" ")
    cells = line.split(" ")
    word = cells[0]
    wordToIndex[word] = int(index)
    #print(tempData)
    wordList = cells[1:]
    #print()
    wordVector = []
    #print(wordList)
    for dimension,value in enumerate(wordList):
        wordVector.append(float(value))
        
    wordsVectorList.append(wordVector)
  #print(i)
  wordDatabaseVectors = np.array(wordsVectorList,dtype='f')
  return (wordToIndex,wordDatabaseVectors)

def convertWordDictToIndex(wordDict):
  wordIndexDict = {}
  for word in wordDict.keys():
    wordIndexDict[wordDict[word]] = word
  return wordIndexDict

def initialiseSimilarity(listOfRow):
  
  multiplied = np.multiply(listOfRow,listOfRow)
  denominator1 = np.sum(multiplied, axis=1)
  sqdenominator1 = np.sqrt(denominator1)
  
  def getSimilarityVector(row):
    numerator = np.dot(listOfRow,np.transpose(row))
    
    #transpose = np.transpose(indexToWordsVector)
    #denominator1a = np.dot(indexToWordsVector,transpose)
    # too many rows to do dotproduct, will generate memory error

    denominator2 = np.dot(row,np.transpose(row))
    sqdenominator2 = np.sqrt(denominator2)
    denominator = sqdenominator1*sqdenominator2
    ratio = numerator / denominator
    #print(numerator)
    #descendingList = np.argsort(ratio)[::-1]
    return ratio
  return getSimilarityVector

def initialiseCosineSimilarity(listOfBase):
  
  sqrtDenominatorList = []
  for listOfRow in listOfBase:
    print(listOfRow.shape)
    multiplied = np.multiply(listOfRow,listOfRow)
    
    denominator1 = np.sum(multiplied, axis=1)
    sqdenominator1 = np.sqrt(denominator1)
    sqrtDenominatorList.append(sqdenominator1)
  
  if True:
    def getSimilarityList(rows):
      numeratorList = []
      numerator = None
      for row in rows:
        numerator = row
        for listOfRow in listOfBase:
          numerator = np.dot(listOfRow,np.transpose(numerator))

        denominator2 = np.dot(row,np.transpose(row))
        sqdenominator2 = np.sqrt(denominator2)
        sqrtDenominatorList.append(sqdenominator2)
      
      sumDenominator = np.prod(sqrtDenominatorList)
      print(numerator)
      
      ratio = numerator / sumDenominator
      
      return ratio
    return getSimilarityList

if False:
  def getSimilarityList2(row,listOfRow):
      numerator = np.dot(listOfRow,np.transpose(row))

      multiplied = np.multiply(listOfRow,listOfRow)
      denominator1 = np.sum(multiplied, axis=1)
      sqdenominator1 = np.sqrt(denominator1)

      denominator2 = np.dot(row,np.transpose(row))
      sqdenominator2 = np.sqrt(denominator2)
      denominator = sqdenominator1*sqdenominator2
      ratio = numerator / denominator
      
      return ratio

def dotProduct(row1,row2):
  print("row1:",row1)
  print("row2:",row2)
  denominator = np.multiply(row1,row2)
  print(denominator)
  return denominator
  
def listWords(wordIndexnp,database,size=1):
  results = []
  if size == 0 or size > len(database.keys()):
    size = len(database.keys())
  wordIndexList = wordIndexnp.tolist()
  for i,wordIndex in zip(range(size), wordIndexList ):
    results.append(database[wordIndex])
  return results
  
def getDescendingList(datalist):
  #argsort always return ascending order, [::-1] to reverse order
  resultsList = np.argsort(datalist)[::-1]
  return resultsList
  #return np.argsort(datalist)[::-1]

def initialiseGetWord(wordsToIndex,dbVector):
  def getWordVector(word):
    try:
      index = wordsToIndex[word]
    except KeyError:
      print("cannot find word", word)
      exit()
    return dbVector[index]
  return getWordVector

def initialiseGetNeighbours( getWordFunc , getSimilarityListFunc,indexToWord ):
  def getNeighbours(word=None,size=10,v=None):
    if v is None:
      selectedWordVector = getWordFunc(word)
    else:
      selectedWordVector = v
    listOfSimilarity =  getSimilarityListFunc(selectedWordVector)
    descendingList = getDescendingList(listOfSimilarity)
    # first item will always be the word itself
    return listWords(descendingList, indexToWord,size+1)[1:]
    
  return getNeighbours

def initialiseGetWordsNearMe(getWordsNearWordsFunc):
  def getWordsNearMe(me,size=10):
    neighboursList = getWordsNearWordsFunc([me],size)
    
    return neighboursList
  return getWordsNearMe

def initialiseGetWordsNearWords(getNeighboursFunc):
  def getWordsNearWords(wordsList,size=10):
    results = []
    for word in wordsList:
      neighboursList = getNeighboursFunc(word,size)

      for neighbourWord in neighboursList:
        neighboursList = getNeighboursFunc(neighbourWord,size)
        if neighboursList[0] in wordsList:
          results.append(neighbourWord)
    
    return list(set(results))
  return getWordsNearWords


if __name__=="__main__":
  import time
  #filename = "glove.6B.50d"
  filepath = "trained_embedding.txt"
  
  size = 1
  f = loadfile(filepath)
  closeNeighbourfilename = "closeNeighbourSize.yaml"
  closeNeighbourDict = matrix.load(closeNeighbourfilename)
  
  wordsToIndex, dbVector = convertFiletoMatrix(f)
  indexToWord = convertWordDictToIndex(wordsToIndex)
  getSimilarityVector = initialiseSimilarity(dbVector)
  #getSimilarityList = initialiseCosineSimilarity(dbVector)
  getWordVector = initialiseGetWord(wordsToIndex,dbVector)
  getNeighbours = initialiseGetNeighbours(getWordVector,getSimilarityVector,indexToWord)

  getWordsNearWords = initialiseGetWordsNearWords(getNeighbours)
  getWordsNearMe = initialiseGetWordsNearMe(getWordsNearWords)

  getSimilarityGroupList = initialiseCosineSimilarity([dbVector])
  
  setting = closeNeighbourDict.get('settings',{})
  closeNeighbourListDict = closeNeighbourDict.get('c',{})
  if buildcache:
    if not setting.get('size',-1) == size or True:
      setting['size'] = size
      closeNeighbourDict['setting'] = setting
      print("loading new closeNeighbourDict")
      for i,word in enumerate(wordsToIndex.keys()):
        if not word in closeNeighbourListDict.keys():
          closeNeighbourListDict[word] = getNeighbours(word,size)
          if (i > 0 and i % 1000 == 0):
            print(i,"save")
            closeNeighbourDict['c']=closeNeighbourListDict
            matrix.save(closeNeighbourfilename,closeNeighbourDict)

    closeNeighbourDict['c']=closeNeighbourListDict
    matrix.save(closeNeighbourfilename,closeNeighbourDict)
  t0 = time.time()
  word = "mercedes"
  #word2 = "read"
  # psychology, physics, words, flute, trading
  if True:
    print("neighbours:",getNeighbours(word),50)
    print("words near me:",getWordsNearMe(word),50)

  #print(getWordsNearWords(["a","an"]))
  if crawl:
    tempWordList = []
    resultsWordList = [word]
    while set(tempWordList) != set(resultsWordList):
      
      tempWordList.extend(resultsWordList)
      tempWordList = list(set(tempWordList))
      resultsWordList.extend(getWordsNearWords(tempWordList,50))    
      resultsWordList = list(set(resultsWordList))
      print("begin", tempWordList) 
      print("end", resultsWordList)
    print("cluster",resultsWordList)
  

  t1 = time.time()


  print("time taken",t1-t0)

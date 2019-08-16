import similarity
import matrix
# for embedding that is big, this generates a cache that of nearest neighbours that can be query quickly instead of recalculations
if __name__=="__main__":
  
  closeNeighbourfilename = "cache.yaml"
  savefilename = "onlySimilarNeighbour.yaml"
  
  closeNeighbourDict = matrix.load(closeNeighbourfilename)
  closeNeighbourDict = closeNeighbourDict['c']
  wordsList = closeNeighbourDict.keys()
  wordDict = {}
  resultList = []
  # create a list from wordsList to a list of words with a corresponding available key
  for word in wordsList:
    wordDict[word] = 1
  # run through the words
  for i,word in enumerate(wordDict.keys()):
    if wordDict[word] == 0:
      continue
    compareWord = closeNeighbourDict[word][0]
    
    if closeNeighbourDict[compareWord][0] == word:
      wordDict[word] = 0
      wordDict[compareWord] = 0
      resultList.append((word,compareWord))

    else:
      wordDict[word] = 0
    
      
  # check if word is available
  # if available, check if word is equivalent to corresponding word, else go to next available word
  # 
  # yes, mark them unavailable and use both words to create a set and save into a list
  # go to the next available word 
  #do some simple statistics count
  # save the list
  print(len(resultList))
  matrix.save(savefilename,resultList)

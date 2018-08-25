import pycor.speechmodel as sm
from pycor import langmodel, korutils 


def printSentences(sentence_array):
    for sentence in sentence_array:
        for word in sentence:
            print(word.text, end=" ")
        print()

def getKeywords(words):
    kwdset = set()
    for word in words:
        if word.bestpair:
            kwdset.add(word.bestpair.head.text)
        else:
            kwdset.add(word.text)
    return kwdset

class SentenceWrap:
    def __init__(self, sentence, count, keywords, index):
        self.sentence = sentence
        self.count = count
        self.keywords = keywords
        self.index = index
        
class DocResolver:
    ESC_WORDCOUNT_TAGS = set(['MAG','MAJ','MM','DN','NP','NNB', 'PT','QS','QE','QM','VOID','EC','CL','SC','Y'])

    def __init__(self):
        print("Init DocResolver")
        self.wordmap = None
        
    
    def setwordmap(self, wordmap):
        self.wordmap = wordmap
    
    def extractKeywords(self,words_array, rate=0.05):
        countmap = {}
        total = 0
        maxcnt = 0
        for words in words_array:
            for word in words :
                if word.bestpair:
                    head = word.bestpair.head
                    if len (self.ESC_WORDCOUNT_TAGS & head.pos) > 0:
                        continue
                    # head.freq()
                    count = countmap.get(head)
                    if count:
                        count += 1
                    else:
                        count = 1
                    countmap[head] = count
                    if count > maxcnt:
                        maxcnt = count
                    total += 1

        avg = (total / len(countmap)) 
        threashold = (maxcnt - avg) * rate + avg

        selected = {}
        for head, count in countmap.items():
            if head.frequency> 0 and head.occurrence()>1:
                if count >= threashold  or (count/head.frequency > rate*10) :
                    selected[head] = count 
        return selected

    def filterSentence(self, sentence, keywords):
        hasEFN = False
        for word in sentence:
            pair = word.bestpair
            
            if pair:
                hasEFN = ('EFN' in pair.tags or 'JKP' in pair.tags)
                if hasEFN:
                    break
        
        if not hasEFN:
            return
        
        return sentence

    def abstractDocument(self, keywords, words_array , sentenceCount=3):
        kwdLen = len(keywords)
        # threashold = int(kwdLen/rate)
        # if(threashold>4):
        #     threashold = int(kwdLen/(rate+1))

        sentenceWrapList = []

        for index, sentence in enumerate(words_array):
            count = 0
            for word in sentence:
                if word.bestpair:
                    head = word.bestpair.head
                    if head in keywords:
                        count += keywords[head]
            
            sent = self.filterSentence(sentence, keywords)
            if sent:
                kwds = getKeywords(sentence)
                sentenceWrapList.append( SentenceWrap(sentence, count, kwds, index) )
                
        sortedlist = sorted(sentenceWrapList, key=lambda wrap:wrap.count, reverse=True)

        # print("Sentence Count:", sentenceCount)
        
        sentence_array_temp = []

        for index, sentenceWrap in enumerate(sortedlist[:int(sentenceCount*1.5)]):
            keywords = sentenceWrap.keywords
            dup = False
            for other in sortedlist[:index]:
                if len(other.keywords & keywords) > int(len(keywords) * 0.7) :
                    dup = True
                    break
            if not dup :
                sentence_array_temp.append(sentenceWrap)
        
        sortedTemplist = sorted(sentence_array_temp, key=lambda wrap:wrap.index)
        sentence_array = []
        for sentenceWrap in sortedTemplist[:sentenceCount]:
            sentence_array.append(sentenceWrap.sentence)

        # printSentences(sentence_array)

        return sentence_array

    # words_array_list
    def mergeDocuments(self, words_array_list , rate=0.05, count=5):
        merged_words_list = []
        for words_array in words_array_list:
            merged_words_list.extend(words_array)

        mergeRate = rate * (len(words_array_list))

        keywords = self.extractKeywords(merged_words_list, rate)

        print(keywords)

        return self.abstractDocument(keywords, merged_words_list, count)
            

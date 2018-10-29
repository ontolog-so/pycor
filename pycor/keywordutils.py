import pycor.speechmodel as sm
from pycor import morpheme, korutils 


def printSentences(sentences):
    for sentence in sentences:
        print(_toTextWordGroup(sentence))


def _toTextWordGroup(wordgroup):
    aline =[]
    for pair in wordgroup.pairs:
        if issubclass(type(pair), sm.WordGroup):
            if type(pair) is sm.Quote:
                if pair.first:
                    aline.append(pair.first)
                aline.append( _toTextWordGroup(pair) )
                if pair.last:
                    aline.append(pair.last)
            else:
                aline.append( _toTextWordGroup(pair) )
        else:
            aline.append( pair.text )
    # print(aline)
    return ' '.join(aline)


def getKeywords(wordgroup):
    kwdset = set()
    for pair in wordgroup.pairs:
        if issubclass(type(pair), sm.WordGroup):
            kwdset.update( getKeywords(pair) )
        else:
            kwdset.add(pair.head.text)
    return kwdset

class SentenceWrap:
    def __init__(self, sentence, count, keywords, index):
        self.sentence = sentence
        self.count = count
        self.keywords = keywords
        self.index = index
        
class KeywordUtils:
    ESC_WORDCOUNT_TAGS = set(['MAG','MAJ','MM','DN','NP','NNB', 'PT','QS','QE','QM','VOID','EC','CL','SC','Y'])

    def __init__(self):
        print("Init DocResolver")
        self.wordmap = None
        
    
    def setwordmap(self, wordmap):
        self.wordmap = wordmap
    
    def __countHeadInSentence(self, sentence, countmap):
        for pair in sentence.pairs :
            if issubclass(type(pair), sm.WordGroup):
                self.__countHeadInSentence(pair,countmap)
            else:
                head = pair.head
                if len (self.ESC_WORDCOUNT_TAGS & head.pos) > 0:
                    continue
                # head.freq()
                count = countmap.get(head)
                if count:
                    count += 1
                else:
                    count = 1
                countmap[head] = count
        
    def extractKeywords(self, sentence_array, rate=0.05):
        countmap = {}
        for sentence in sentence_array:
            self.__countHeadInSentence(sentence,countmap)

        total = 0
        maxcnt = 0

        for count in countmap.values():
            total += count
            if count > maxcnt:
                maxcnt = count
        
        avg = (total / len(countmap)) 
        threashold = (maxcnt - avg) * rate + avg

        print("[countmap]", countmap)
        selected = {}
        for head, count in countmap.items():
            if head.frequency> 0 and head.occurrence()>1:
                if count >= threashold  or (count/head.frequency > rate*10) :
                    selected[head] = count 
        print("[selected]", selected)
        return selected

    def filterSentence(self, sentence, keywords):
        hasEFN = False
        for pair in sentence.pairs:
            if type(pair) is sm.Pair:
                hasEFN = ('EFN' in pair.tags or 'JKP' in pair.tags)
                if hasEFN:
                    break
        
        if not hasEFN:
            return
        
        return sentence

    def __countHeadInKeywords(self, keywords, wordgroup):
        count = 0
        for pair in wordgroup.pairs:
            if issubclass(type(pair), sm.WordGroup):
                self.__countHeadInKeywords(keywords, pair)
            else:
                head = pair.head
                if head in keywords:
                    count += keywords[head]
        return count

    def abstractDocument(self, keywords, sentences , sentenceCount=3):
        kwdLen = len(keywords)
        # threashold = int(kwdLen/rate)
        # if(threashold>4):
        #     threashold = int(kwdLen/(rate+1))

        sentenceWrapList = []

        for index, sentence in enumerate(sentences):
            count = self.__countHeadInKeywords(keywords, sentence)
            
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
            

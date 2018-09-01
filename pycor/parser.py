import re
import os
import pycor.speechmodel as sm
from pycor import langmodel, korutils , docresolver

class Quote:
    def __init__(self,start,end):
        self.start = start
        self.end = end

_quoteclues = {
    '「':Quote('「','」'),
    '‘':Quote('‘','’'),
    '“':Quote('“','”'),
    '"':Quote('"','"'),
    '(':Quote('(',')'),
    '[':Quote('[',']'),
    '{':Quote('{','}'),
    '\'':Quote('\'','\''),
    '\"':Quote('\"','\"'),
    '《':Quote('《','》'),
    '〈':Quote('〈','〉'),
    '⟪':Quote('⟪','⟫'),
    '｢':Quote('｢','｣'),
    '＜':Quote('＜','＞'),
    '［':Quote('［','］'),
    '（':Quote('（','）'),
    '『':Quote('『','』'),
    '<':Quote('<','>')   
    }

def isdigit(text, index):
    if index<0 or len(text) -1 < index:
        return False
    return text[index].isdigit() 

##################################################
#  어절 단위 텍스트 커서  
##################################################
class WordTokens :
    token_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")
    non_kor_pattern = re.compile("([^가-힣]+)")
    def __init__(self, text):
        self.set(text)
        
    def set(self, text):
        self.text = text
        self.curidx = None
        self.tokens = []
        length = len(text)
        idx = 0
        
        while idx < length:
            if korutils.isKorChar(text[idx]) :
                self.tokens.append(text[idx])
                idx += 1
            else :
                # 한글이 아닐 때
                m = self.non_kor_pattern.search(text, idx)
                self.tokens.append(text[m.start(): m.end()])
                idx = m.end()
    
    def setPos(self, index):
        self.curidx = index
        return self
    
    def length(self):
        return len(self.tokens)
    
    def fromEnd(self):
        return len(self.tokens) - self.curidx
    
    def current(self, toIdx=None):
        if toIdx is None:
            return self.tokens[self.curidx]
        else :
            if toIdx > self.curidx:
                return self.tokens[self.curidx:toIdx]
            else:
                return self.tokens[toIdx:self.curidx+1]

    def next(self):
        if self.curidx is None:
            self.curidx = -1
        
        if self.curidx < self.length()-1:
            self.curidx += 1
            return self.tokens[self.curidx]
        else:
            return None
        
    def peekNext(self):
        idx = self.curidx
        if idx is None:
            idx = -1
        
        if idx < self.length()-1:
            idx += 1
            return self.tokens[idx]
        else:
            return None
        
        pre = wordTokens.peekPrev()

    def prev(self):
        if self.curidx is None:
            self.curidx = self.length()
        
        if self.curidx > 0:
            self.curidx -= 1
            prev = self.tokens[self.curidx]

            #if pair and len(pair.head)>len(prev):
            #    return pair.head[len(pair.head)-len(prev)]

            return prev
        else :
            return None
    
    def peekPrev(self):
        idx = self.curidx
        if idx is None:
            idx = self.length()
        
        if idx > 0:
            idx -= 1
            prev = self.tokens[idx]
            
            #if pair and len(pair.head)>len(prev):
            #    return pair.head[len(pair.head)-len(prev)]

            return prev
        else :
            return None
    
    def head(self, idx=None):
        if idx is None:
            idx=self.curidx
        return ''.join(self.tokens[:idx])
    
    def tail(self, idx=None):
        if idx is None:
            idx=self.curidx
        return ''.join(self.tokens[idx:])
    
    def getStr(self, startIdx, endIdx = -1):
        if endIdx > 0:
            return ''.join(self.tokens[startIdx:endIdx])
        else:
            return self.tokens[startIdx]
    
##################################################
#  Class : WordParser 어절 단위 파서 
##################################################
class WordParser:
    token_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")
    non_kor_pattern = re.compile("([^가-힣]+)")
    tail_token_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")
    
    def __init__(self, auxmap = langmodel.auxmap, singlemap=langmodel.singlemap):
        self.auxmap = auxmap
        self.singlemap = singlemap
        self.wordmap = None
        
    def getAuxs(self, token):
        return langmodel.getAuxs(token)
        
    def getStems(self, token):
        return langmodel.getStems(token)
        
    def getSuffixs(self, token):
        return langmodel.getSuffixs(token)
        
    def digest_word(self, wordObj, prevWord, nextWord):
        word = wordObj.text
        if word in self.singlemap:
            sng = self.singlemap[word]
            pair = sm.Pair(word, None).addpos(sng.atag).addtags(sng.atag)
            self.digest_pair(None, wordObj, pair)
            pair.head.addpos(sng.atag)
        else :
            tokens = WordTokens(word)
            self.bisect(tokens, wordObj, prevWord, nextWord)
            
    def bisect(self, wordTokens, wordObj, prevWord, nextWord, cascade=True):
        token = wordTokens.prev()
        if token:
            pairs = []

            worms = self.getAuxs(token)
            if worms:
                curidx = wordTokens.curidx
                for worm in worms :
                    headtails = worm.procede(wordTokens, None, wordObj, None, prevWord, nextWord)
                    if headtails:
                        pairs.extend(headtails)
                    wordTokens.setPos(curidx)
            else :
                head = wordObj.text
                pair = sm.Pair(head, None, 0)
                pairs.append(pair)
            
            for pair in pairs:
                self.digest_pair(wordTokens, wordObj, pair)

        elif cascade :
            self.digest_pair( wordObj, sm.Pair(wordObj.text, None) ) 

            
    ###################################### 
    #  Head, Tail 처리 
    ######################################         
    def digest_pair(self, wordTokens, wordObj, pair):
        if pair is None or pair.head is None:
            #헤드 값이 없으면 그냥 skip
            return
        
        
        h = pair.head.upper() # 영문의 경우 대문자로 변화 
        head = self.wordmap.heads.get(h)
        if head is None:
            head = self.buildhead(wordTokens, h)
            
        head.freq()
        tail = sm._VOID_Tail
        
        if pair.tail:
            t = pair.tail.upper() # 영문의 경우 대문자로 변화 
            tail = self.wordmap.tails.get(t)
            if tail is None:
                tail = self.buildtail(t)

            head.appendtail(tail)
            tail.appendhead(head)
        pair.head = head
        pair.tail = tail
        
        wordObj.addPair(pair)

        
    def buildhead(self, wordTokens, text):
        head = None
        if len(text) == 0:
            head = sm._VOID_Head
        else:
            head = sm.Head(text)
            self.wordmap.heads[text] = head
        return head

    def buildtail(self, text):
        tail = sm.Tail(text, text)
        self.wordmap.tails[text] = tail
        return tail
    
    

#################################################
#  Class : SentenceParser
#################################################
class SentenceParser:
    def __init__(self, wordparser=WordParser(), quoteclues=_quoteclues, wordMap=None):
        self._initimpl(wordparser, quoteclues, wordMap)
        self.verbose = False
        
    def _initimpl(self, wordparser, quoteclues, wordMap=None):
        if wordMap is None:
            wordMap = sm.WordMap(wordparser)
        self.wordmap = wordMap
        self.wordparser = wordparser
        self.quoteclues = quoteclues
        wordparser.wordmap = self.wordmap
    
    def setmodel(self, wordMap):
        self.wordmap = wordMap
        self.wordparser.wordmap = self.wordmap
        self.wordmap.wordparser = wordparser
    
    def loadfile(self, path):
        sentence_array = self._loadfile(path)
        words_array = self.resolveDocument(sentence_array)
        return sentence_array, words_array
    
    def _loadfile(self, path):
        sentence_array = []
        words_array = []

        with open(path, 'r', encoding='utf-8') as file :
            lines = file.readlines()
            
            for row in lines:
                self._readrow(row,sentence_array,words_array)  
                # sentence_array.extend(sentences)
                words_array.clear()
            file.close()
        return sentence_array

    def savemodel(self, path):
        print("Saving Model to",path)
        os.makedirs(path, exist_ok=True)
        self.wordmap.save(path)

    def loadmodel(self, path):
        print("Loading Model from",path)
        self.wordmap.load(path)

    ########################
    #  Read all Document  
    ########################
    def readtext(self, text):
        """
        return Document : sentence_array, words_array
        """
        sentence_array = []
        words_array = []

        for row in text.splitlines():
                self._readrow(row,sentence_array,words_array)  
                words_array.clear()
        
        words_array = self.resolveDocument(sentence_array)
        return sentence_array, words_array

    ########################
    #  라인별 읽기 
    ########################
    def readrow(self,text):
        sentence_array = []
        words_array = []
        self._readrow(text, sentence_array, words_array)
        return sentence_array

    ########################
    #  라인별 읽기 
    ########################
    def _readrow(self,text, sentence_array, words_array):
        length = len(text)
        index = 0
        word = ''
        while index < length:
            ch = text[index]
            if ch in self.quoteclues:
                end = text.find(self.quoteclues[ch].end, index+1)
                word = word.strip()
                if(len(word) > 0):
                    words_array.append(word)
                    
                word = ''

                if end > index:
                    arr = self.readrow(text[index+1:end])
                    words_array.append("[")
                    words_array.extend(arr)
                    words_array.append("]")
                    index = end +1
                else:
                    index +=1 
            else:
                if ch in ['.','?','!',':',';','\n']:
                    if ch == '.' and (isdigit(text, index-1) or isdigit(text, index+1)) :
                        word += ch
                        index += 1
                        continue

                    #print("end sentence.", ch)
                    word = word.strip()
                    if(len(word) > 0):
                        words_array.append(word)
                    words_array.append(ch)
                    word = ''
                    sent = self._buildsentence(words_array)
                    sentence_array.append(sent)
                    words_array.clear()
                #elif ch.isspace():
                elif ch in [' ','　',' ',' ',',','\n','\r']:
                    #32 12288 8194
                    word = word.strip()
                    if(len(word) > 0):
                        words_array.append(word)
                    word = ''
                elif ch in ['-','_']:
                    word += ch
                elif ch.isalpha() or ch.isdigit():
                    word += ch
                index += 1

        word = word.strip()
        if len(word) > 0:
            words_array.append(word)

        if len(words_array) > 0:
            sent = self._buildsentence(words_array)
            sentence_array.append(sent)

        return sentence_array

    
    # words_array를 기반으로 Word 객체 생성하고  Sentence 생성  
    def _buildsentence(self, words_array):
        sentence = sm.Sentence()
        
        wlength = len(words_array)
        windex  = 0
        while windex < wlength:
            word = words_array[windex]
            if type(word) is str :
                word = word.strip()            
                if(len(word) > 0):
                    prev = words_array[windex-1] if windex > 1 else None
                    nxt = words_array[windex+1] if windex < wlength-1 else None
                    
                    sentence.addword( self._getword(word, prev, nxt) )
            elif type(word) is sm.Sentence:
                #print("Sentence", word)
                sentence.addword(word)
            elif word : 
                #print("Other", word)
                sentence.addword(word)
            
            windex += 1
        
        
        return sentence

    def _getword(self, text, prev, nxt):
        word = self.wordmap.getword(text, prev, nxt)
        return word

    def resolveDocument(self, sentence_array):
        words_array = self.scoreDocument(sentence_array)
        return words_array

    def scoreDocument(self, sentence_array) :
        words_array = []
        for sentence in sentence_array:
            words_array.append(self.scoreSentence(sentence))
        
        return words_array
        
    def scoreSentence(self, sentence) :
        words = []
        for word in sentence.words:
            if type(word) is sm.Sentence:
                words.extend(self.scoreSentence(word))
            else :
                self.scoreword(word)
                words.append(word)
        return words


    def scoreword(self, word) :
        if word.bestpair:
            return

        if len(word.particles) > 0:
            maxPart = None
            for part in word.particles:
                if part.head == sm._VOID_Head:
                    part.addpos("VOID")
                
                score = part.score * 2
                hs = 0
                ts = 0

                hs = part.head.occurrence()
                if score<0:
                    hs = hs * 1.3

                if part.tail:
                    ts = part.tail.occurrence()
                
                part.score = hs - (ts*0.09) + (score * 10)

                if maxPart:
                    if part.score > maxPart.score:
                        maxPart = part
                    elif (part.score == maxPart.score) :
                        if (len(part.tags)>len(maxPart.tags)):
                            maxPart = part
                        elif len(part.tags) == len(maxPart.tags) :
                            if len(part.tail.text) > len(maxPart.tail.text):
                                maxPart = part
                else :
                    maxPart = part
            score = (maxPart.score / len(self.wordmap.words))
            if maxPart.head:
                maxPart.head.score += score
            if maxPart.tail:
                maxPart.tail.score += score

            maxPart.head.addpos(maxPart.pos)
            maxPart.tail.addtags(maxPart.tags)
            word.bestpair = maxPart
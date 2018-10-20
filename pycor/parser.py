import re
import os
import pycor.speechmodel as sm
from pycor import morpheme, syntagm, korutils, scoring, classifier, resolver

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

_equivalentclues = {
    '(':Quote('(',')'),
    '[':Quote('[',']'),
    '［':Quote('［','］'),
    '（':Quote('（','）') 
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
#  문장 단위 어절 커서  
##################################################
class SyntagmTokens :
    def set(self,sentence):
        self.sentence = sentence
        self.curidx = None
        self.length = len(sentence.words)
        idx = 0

    def setPos(self, index):
        self.curidx = index
        return self
    
    def fromEnd(self):
        return length - self.curidx
    
    def current(self, toIdx=None):
        if toIdx is None:
            return self.sentence.words[self.curidx]
        else :
            if toIdx > self.curidx:
                return self.sentence.words[self.curidx:toIdx]
            else:
                return self.sentence.words[toIdx:self.curidx+1]

    def next(self, size=1):
        if self.curidx is None:
            self.curidx = -1
        
        if self.curidx < self.length-1:
            self.curidx += 1
            if size > 1:
                nextpos = self.curidx + size 
                tokens = self.sentence.words[self.curidx:nextpos]
                self.curidx = nextpos-1
                return tokens
            else:
                return self.sentence.words[self.curidx]
        else:
            return None
        
    def peekNext(self):
        idx = self.curidx
        if idx is None:
            idx = -1
        
        if idx < self.length-1:
            idx += 1
            return self.sentence.words[idx]
        else:
            return None
        
        pre = wordTokens.peekPrev()

    def peekNexts(self,count):
        idx = self.curidx
        if idx is None:
            idx = -1
        
        if idx < self.length-1:
            idx += 1
            end = idx + count
            return self.sentence.words[idx:end]
        else:
            return None
    
    def prev(self, size=1):
        if self.curidx is None:
            self.curidx = self.length
        
        if self.curidx > 0:
            if size > 1:
                prevpos = self.curidx - size
                tokens = self.sentence.words[prevpos:self.curidx]
                self.curidx = prevpos
                return tokens
            else:
                self.curidx -= 1
                return self.sentence.words[self.curidx]
        else :
            return None
    
    def peekPrev(self):
        idx = self.curidx
        if idx is None:
            idx = self.length
        
        if idx > 0:
            idx -= 1
            prev = self.sentence.words[idx]
            return prev
        else :
            return None
    
    def peekPrevs(self, count):
        idx = self.curidx
        if idx is None:
            idx = self.length

        if idx > 0:
            start = idx - count
            if start < 0 :
                start = 0
            idx -= 1
            prev = self.sentence.words[start:idx]
            return prev
        else :
            return None
    
##################################################
#  Class : WordParser 어절 단위 파서 
##################################################
class WordParser:
    token_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")
    non_kor_pattern = re.compile("([^가-힣]+)")
    tail_token_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")
    
    def __init__(self, auxmap = morpheme.auxmap, singlemap=morpheme.singlemap):
        self.auxmap = auxmap
        self.singlemap = singlemap
        
    def getAuxs(self, token):
        return morpheme.getAuxs(token)
        
    def getStems(self, token):
        return morpheme.getStems(token)
        
    def getSuffixs(self, token):
        return morpheme.getSuffixs(token)
    
    def getword(self, text, prev, nxt,  wordmap):
        word = wordmap.getword(text)
        if word is None:
            word = sm.Word(text)
            self.digest_word(word, prev, nxt, wordmap)
            wordmap.addword(word)
        
        return word


    def digest_word(self, wordObj, prevWord, nextWord, wordmap):
        word = wordObj.text
        if word in self.singlemap:
            sng = self.singlemap[word]
            pair = sm.Pair(word,word, None).addpos(sng.atag).addtags(sng.atag)
            self.digest_pair(None, wordObj, pair, wordmap)
            pair.head.addpos(sng.atag)
        else :
            # v0.0.7
            fromLast = False
            if word in wordmap.heads:
                # word가 heads맵에 이미 등록된 경우 
                head = wordmap.heads[word]
                if head.score>0:
                    pair = sm.Pair(word,word, None)
                    self.digest_pair(None, wordObj, pair, wordmap)
                    return
                else:
                    fromLast = True

            tokens = WordTokens(word)
            self.bisect(tokens, wordObj, prevWord, nextWord, wordmap, fromLast)
            
    def bisect(self, wordTokens, wordObj, prevWord, nextWord, wordmap, fromLast=False):
        token = wordTokens.prev()
        if token:
            pairs = []
            # 0.0.7 zeroPair 
            zeroPair = None
            worms = self.getAuxs(token)

            if fromLast:
                head = wordObj.text
                zeroPair = sm.Pair(wordTokens.text, head, None, 0)
                pairs.append(zeroPair)

            if worms:
                curidx = wordTokens.curidx
                for worm in worms :
                    headtails = worm.procede(wordTokens, None, wordObj, zeroPair, prevWord, nextWord)
                    if headtails:
                        pairs.extend(headtails)
                    wordTokens.setPos(curidx)
            
            if len(pairs) == 0:
                head = wordObj.text
                zeroPair = sm.Pair(wordTokens.text,head, None, 0)
                pairs.append(zeroPair)

            for pair in pairs:
                self.digest_pair(wordTokens, wordObj, pair, wordmap)

            
    ###################################### 
    #  Head, Tail 처리 
    ######################################         
    def digest_pair(self, wordTokens, wordObj, pair, wordmap):
        if pair is None or pair.head is None:
            #헤드 값이 없으면 그냥 skip
            return
            
        h = pair.head.upper() # 영문의 경우 대문자로 변화 
        head = wordmap.heads.get(h)
        if head is None:
            head = self.buildhead(wordTokens, h, wordmap)
            
        head.freq()
        tail = sm._VOID_Tail
        
        if pair.tail:
            t = pair.tail.upper() # 영문의 경우 대문자로 변화 
            tail = wordmap.tails.get(t)
            if tail is None:
                tail = self.buildtail(t, wordmap)
            head.appendtail(tail)
            tail.appendhead(head)
        elif head.occurrence() == 0:
            head.occ = 1
            
        pair.head = head
        pair.tail = tail
        
        wordObj.addPair(pair)

        
    def buildhead(self, wordTokens, text, wordmap):
        head = None
        if len(text) == 0:
            head = sm._VOID_Head
        else:
            head = sm.Head(text)
            wordmap.heads[text] = head
        return head

    def buildtail(self, text, wordmap):
        tail = None

        if len(text) == 0:
            tail = sm._VOID_Tail
        else :
            tail = sm.Tail(text)
            
        wordmap.tails[text] = tail
        return tail
    
    

#################################################
#  Class : SentenceParser
#################################################
class SentenceParser:
    def __init__(self, wordparser=WordParser(), quoteclues=_quoteclues, equivalentclues=_equivalentclues , 
        scorefunc=scoring.default_scorepair, classifyfunc=classifier.def_classify, wordMap=None):
        self._initimpl(wordparser, quoteclues, equivalentclues, scorefunc, classifyfunc, wordMap)
        self.verbose = False
        self.resolvers = []
        
    def _initimpl(self, wordparser, quoteclues, equivalentclues, scorefunc, 
            classifyfunc, wordMap=None):
        if wordMap is None:
            wordMap = sm.WordMap()
        self.wordmap = wordMap
        self.scorefunction = scorefunc
        self.classifyfunction = classifyfunc
        self.wordparser = wordparser
        self.quoteclues = quoteclues
        self.equivalentclues = equivalentclues
        
    def addresolver(self, resolver):
        self.resolvers.append(resolver)

    def removeresolver(self, resolver):
        self.resolvers.remove(resolver)

    def setmodel(self, wordMap):
        self.wordmap = wordMap


    def resolveword(self, text, debug=False):
        word = self.wordparser.getword(text, None, None,  self.wordmap)
        self.scoreword(word, force=True)

        if debug:
            self.debugword(word)

        return word

    def debugword(self, word):
        if len(word.particles) == 0:
            print(word.text, 'X')
        for part in word.particles:
            h = part.head.text if part.head else ''
            t = part.tail.text if part.tail else ''
            print(word.text, h, t, part.score, part.tags, part.pos)

    def loadfile(self, path, context=None):
        sentence_array = self._loadfile(path)
        self.resolveDocument(sentence_array, context)
        return sentence_array
    
    def _loadfile(self, path):
        sentence_array = []
        words_array = []

        with open(path, 'r', encoding='utf-8') as file :
            lines = file.readlines()
            
            for row in lines:
                self._readrow(row,sentence_array,words_array, isquote=False)  
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

    def loaddic(self, dic_path):
        print("Loading Dictionary from",dic_path)
        self.wordmap.readheads(dic_path)

    ########################
    #  Read all Document  
    ########################
    def readtext(self, text, context=None):
        """
        return Document : sentence_array, words_array
        """
        sentence_array = []
        words_array = []

        for row in text.splitlines():
                self._readrow(row,sentence_array,words_array, isquote=False)  
                words_array.clear()
        
        self.resolveDocument(sentence_array,context)
        return sentence_array

    ########################
    #  라인별 읽기 
    ########################
    def readrow(self,text, isquote=False):
        sentence_array = []
        words_array = []
        self._readrow(text, sentence_array, words_array, isquote)
        return sentence_array

    ########################
    #  라인별 읽기 
    ########################
    def _readrow(self,text, sentence_array, words_array, isquote):
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
                    arr = self.readrow(text[index+1:end],isquote=True)
                    if len(arr) > 0:
                        arr[0].first = ch
                        arr[0].last = self.quoteclues[ch].end

                    if ch in self.equivalentclues:
                        if len(arr) > 1:
                            words_array.extend(arr)
                        elif len(arr) == 1:
                            arr[0].quotetype = sm.QUOTE_TYPE_EQUIV
                            words_array.append(arr[0])
                    else:
                        words_array.extend(arr)

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
            sent = self._buildsentence(words_array, isquote)
            sentence_array.append(sent)

        return sentence_array

    
    # words_array를 기반으로 Word 객체 생성하고  Sentence 생성  
    def _buildsentence(self, words_array, isquote=False):
        sentence = sm.Sentence()
        if isquote:
            sentence = sm.Quote()
        else:
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
            elif issubclass(type(word), sm.WordGroup):
                #print("WordGroup", word)
                sentence.addword(word)
            elif word : 
                #print("Other", word)
                sentence.addword(word)
            
            windex += 1
        
        return sentence

    def _getword(self, text, prev, nxt):
        word = self.wordparser.getword(text, prev, nxt,self.wordmap)
        return word

    def resolveDocument(self, sentence_array, context=None):
        if context is None:
            context = self.wordmap

        documentContext = sm.DocumentContext(context)
        syntagmTokens = SyntagmTokens()

        for sentence in sentence_array:
            self.scoreWordGroup(sentence, documentContext)
            syntagmTokens.set(sentence)
            self.resolveSentence(syntagmTokens, documentContext)

        self._doresolver(sentence_array, documentContext)

    def _doresolver(self, sentence_array, context):
        for resolver in self.resolvers:
            resolver.resolveDocument(sentence_array, context)

    def resolveSentence(self, syntagmTokens, documentContext):
        word = syntagmTokens.prev()
        if word :
            print("(-1)", syntagmTokens.curidx, word.text)

            words = syntagmTokens.prev(2)
            print("(-2)", syntagmTokens.curidx, words)

            words = syntagmTokens.prev(3)
            print("(-3)", syntagmTokens.curidx, words)

            syntagmTokens.setPos(-1)

            word = syntagmTokens.next()
            print("(+1)", syntagmTokens.curidx, word.text)
            
            words = syntagmTokens.next(2)
            print("(+2)", syntagmTokens.curidx, words)

            words = syntagmTokens.next(3)
            print("(+3)", syntagmTokens.curidx, words)


    def scoreWordGroup(self, wordgroup, documentContext) :
        for index, word in enumerate(wordgroup.words):
            if issubclass(type(word), sm.WordGroup):
                wordgroup.addpair( self.scoreWordGroup(word, documentContext) )
            else :
                prevWords = wordgroup.words[:index]
                nextWords = wordgroup.words[index+1:]
                self.classifyHeads(word)
                pair = self.scoreword(word, prevWords, nextWords, force=True)
                wordgroup.addpair(pair)
                documentContext.countHead(pair.head)
        return wordgroup

    def classifyHeads(self,word, force=True):
        for pair in  word.particles:
            self.classifyfunction(pair.head, force)

    def scoreword(self, word, prevWords=None, nextWords=None, force=False) :
        if word.bestpair and not(force):
            return word.bestpair

        if len(word.particles) == 0:
            raise Exception("No Pair", word.text)
        else:
            maxPart = None
            for part in word.particles:
                self.scorefunction(part, word, self.wordmap, prevWords, nextWords)
                
                if maxPart:
                    if part.score > maxPart.score:
                        maxPart = part
                    elif (part.score == maxPart.score) :
                        if len(part.tags) == len(maxPart.tags) :
                            if len(part.tail.text) > len(maxPart.tail.text):
                                maxPart = part
                        elif (len(part.tags)>len(maxPart.tags)):
                            maxPart = part
                else :
                    maxPart = part
                    
            score = maxPart.score
            
            if maxPart.head:
                # hscore = maxPart.head.score 
                # if maxPart.head.score > 0:
                #     hscore += score / maxPart.head.score
                # else:
                #     hscore += score
                # maxPart.head.score = hscore
                maxPart.head.score += score
                maxPart.head.addpos(maxPart.pos)

            if maxPart.tail and maxPart.tail != sm._VOID_Tail:
                tscore = maxPart.tail.score + score
                maxPart.tail.score = tscore /2
                maxPart.tail.addtags(maxPart.tags)

            word.bestpair = maxPart

            return word.bestpair
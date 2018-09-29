#####################################################################
# 
#   텍스트의 구성 요소 정보  
# 
#####################################################################
import re
import time
import csv
import pycor.korutils


def sortParticle(particle):
    return particle.text

########################
#  어절 정보 객체 
########################
class Word:
    def __init__(self,text):
        self.text = text
        self.particles = [] 
        self.prevnexts = []
        self.bestpair = None
    
    def type(self):
        return "W"
    
    def addprevnext(self, prev,next):
        self.prevnexts.append(PrevNext(prev,next))
    
    def addPair(self, pair):
        self.particles.append(pair)
        return pair
    
    def clear(self):
        if self.bestpair:
            del self.particles[:]

        del self.prevnexts[:]

class Pair:
    def __init__(self,head, tail, score=0.0, ambi=False):
        self.head = head
        self.tail = tail
        self.score = score
        self.ambi = ambi
        self.pos = set()
        self.tags = []
        
    def __repr__(self) :
        return str(self.head) + ":" + str(self.tail) 
    
    def ambiguous(self, ambi=True):
        self.ambi = ambi
        return self

    def addpos(self, pos):
        if pos:
            if type(pos) is list:
                self.pos.update(pos)
            elif type(pos) is set:
                self.pos.update(pos)
            else:
                self.pos.add(pos)

        return self

    def addtags(self, tags):
        if tags:
            if type(tags) is list:
                self.tags.extend(tags)
            else:
                self.tags.append(tags)
        return self

class PrevNext:
    def __init__(self,prev,next):
        self.prevword = prev
        self.nextword = next

class WordGroup:
    def __init__(self):
        self.words = [] 
    def type(self):
        return "S"
    
    def text(self):
        text = ''
        for w in self.words:
            if issubclass(type(w), WordGroup):
                text += w.text() + ' '
            else:
                text += w.text + ' '
        return text
    
    def addword(self, word):
        #print ("append ", type(word) , word)
        self.words.append(word)


SENTENCE_TYPE_QUOTE = 'QUOTE'
SENTENCE_TYPE_EQUIV = 'EQUIV'

class Sentence(WordGroup):
    def __init__(self):
        super().__init__()
        self.senttype = None
    
    


# class Document:
#     def __init__(self, sentence_array, words_array):
#         self.sentence_array = sentence_array 
#         self.words_array = words_array




########################
#  Head
########################
class Head:
    def __init__(self,text):
        self.text = text
        self.score = 0.0
        self.occ = 0
        self.frequency = 0
        self.tails = []
        self.proto = None
        # self.equivalent = None
        self.pos = set()
        
    def type(self):
        return "H"
    
    def __repr__(self) :
        return self.text 
    
    def appendtail(self, tail):
        if not(tail in self.tails):
            self.tails.append(tail)
    
    def freq(self):
        self.frequency += 1

    def occurrence(self):
        return self.occ + len(self.tails)
    
    def addpos(self, pos):
        if pos:
            if type(pos) is list:
                self.pos.update(pos)
            elif type(pos) is set:
                self.pos.update(pos)
            else:
                self.pos.add(pos)

        return self

_VOID_Head = Head(u'').addpos('VOID')

class Keyword(Head):
    def __init__(self, text):
        super().__init__(text)
    

########################
#  Tail
########################
class Tail():
    def __init__(self, text):
        self.text = text
        self.score = 0.0
        self.occ = 0
        self.heads = []
        self.tags = set()
        
    def type(self):
        return "T"
    
    def __repr__(self) :
        return self.text + ":" + str(self.tags) + ":" + str(self.occurrence())
    
    def appendhead(self, head):
        if not(head in self.heads):
            self.heads.append(head)
        
    def occurrence(self):
        return self.occ + len(self.heads)
    
    def addtags(self, tags):
        if tags:
            if type(tags) is list:
                self.tags.update(tags)
            else:
                self.tags.add(tags)
        return self
    
_VOID_Tail = Tail(u'')  


# 연어의 구성 요소 
class CollocationHead(Head):
    def __init__(self, texts):
        super().__init__(' '.join(texts))
        self.texts = texts
        self.score = 1
    
    def tp():
        return "HEAD"
    

class ContextWrapper:
    def __init__(self, parent):
        self.parent = parent

    def addword(self, wordObj):
        self.parent.addword(wordObj)
        return wordObj

    def getword(self, text):
        return self.parent.getword(text)
    
    def registerKeyword(self, text, pos):
        return self.parent.registerKeyword(text, pos)

    def getcollocation(self, text):
        return self.parent.getcollocation(text)

    def addcollocation(self, collocation):
        self.parent.addcollocation(collocation)

    def getOrNewHead(self, text):
        return self.parent.getOrNewHead(text)

    def save(self, modelDir):
        self.parent.save(modelDir)

    def load(self, modelDir):
        self.parent.load(modelDir)
        
########################
#  단어 정보 객체 
########################
class WordMap :
    def __init__(self, wordlimit=200000):
        super().__init__()
        self.words = {}
        self.heads = {}
        self.tails = {}
        self.collocations = {}
        self.wordlimit = wordlimit
    
    def addword(self, wordObj):
        text = wordObj.text
        word = self.words.get(text)
        if word is None:
            self.words[text] = wordObj
        else :
            raise Exception("Word '" + text + "' is already registered.")
        return wordObj

    def getword(self, text):
        word = self.words.get(text)
        return word
    
    def getOrNewHead(self, text):
        head = self.heads.get(text)
        if head is None:
            head = Head(text)
            self.heads[text] = head
        return head

    def getcollocation(self, text):
        return self.collocations.get(text)

    def addcollocation(self, collocation):
        if self.collocations.get(collocation.text) is None:
            self.collocations[collocation.text] = collocation

    # 명사, 부사 등 조사/어미가 없는 단일 단어 등록  
    def registerKeyword(self, text, pos):
        word = self.words.get(text)
        if word is None:
            word = Word(text)
            head = self.getOrNewHead(text)
            head.addpos(pos)
            pair = word.addPair(Pair(head,_VOID_Tail))
            word.bestpair = pair
            self.words[text] = word
        elif word.bestpair:
            if word.bestpair.tail != _VOID_Tail:
                head = self.getOrNewHead(text)
                head.addpos(pos)
                pair = word.addPair(Pair(head,_VOID_Tail))
                word.bestpair = pair
        else:
            for pair in word.particles:
                if pair.tail == _VOID_Tail:
                    word.bestpair = pair
                    return word
            head = self.getOrNewHead(text)
            head.addpos(pos)
            pair = word.addPair(Pair(head,_VOID_Tail))
            word.bestpair = pair
        return word
    
    def save(self, modelDir):
        self.writeheads(path=modelDir + "/heads.csv")
        self.writetails(path=modelDir + "/tails.csv")
        self.writecollocations(path=modelDir + "/collocations.csv")
        self.clearheads()

    def load(self, modelDir):
        self.readheads(path=modelDir + "/heads.csv")
        self.readtails(path=modelDir + "/tails.csv")
        
    # words 비우기 
    def clearwords(self):
        print("Clear words size:", len(self.words))
        self.words.clear()

    def clearheads(self):
        headlist = list(self.heads.values())
        for head in headlist:
            if head.score != 0 :
                del(self.heads[head.text])
        print("Clear Heads:", len(self.heads), "remains.")

    #####################################################################
    #  결과 파일 출력 
    #####################################################################
    #########################
    ## 추출 단어 출력 
    #########################
    def writewords(self, path="model/words.csv"):
        starttime = time.time()
        with open(path, 'w', encoding='utf-8') as csvfile :
            writer = csv.writer(csvfile)
            for word in self.words:
                writer.writerow([word.text, word.prevnext.prev, ])
            csvfile.close()
        print("Save ", path,  "  소요시간:" , round(time.time() - starttime, 3))
    
    #########################
    ## Head/tail 출력 내부 함수 
    #########################
    def _write_particles(self, path, parts, bhead, sorter=None, reversed=False):
        starttime = time.time()
        with open(path, 'w', encoding='utf-8') as csvfile :
            writer = csv.writer(csvfile)
            list = parts.values()
            if sorter:
                list = sorted(parts.values(), key=lambda particle: sorter(particle), reverse=reversed)

            if bhead:
                for part in list:
                    if part.score:
                        writer.writerow([part.text, '+'.join(part.pos), part.score, part.occurrence(), part.frequency, part.proto])
            else:
                for part in list:
                    if part.score:
                        writer.writerow([part.text, '+'.join(part.tags), part.score, part.occurrence()])
            csvfile.close()
        print("Save ", path,  "  소요시간:" , round(time.time() - starttime, 3))

    
    #########################
    ## Head 출력 
    #########################
    def writeheads(self, path="model/heads.csv", sorter=sortParticle, reversed=False):
        self._write_particles(path, self.heads, True, sorter, reversed)
        
    def writecollocations(self, path="model/collocations.csv", sorter=sortParticle, reversed=False):
        self._write_particles(path, self.collocations, True, sorter, reversed)
        
    #########################
    ## Head 로딩 
    #########################
    def readheads(self, path="model/heads.csv"):
        starttime = time.time()
        with open(path, 'r', encoding='utf-8') as csvfile :
            reader = csv.reader(csvfile)
            for row in reader:
                text = row[0]
                pos = row[1].split('+')
                score = 1
                occurrence = 10
                frequency = 1
                proto = None

                length = len(row)

                if length>2:
                    score = float(row[2])
                    occurrence = int(score * 10)
                    if length > 3:
                        occurrence = int(row[3])
                        if length > 4:
                            frequency = int(row[4])
                            if length > 5:
                                proto = str(row[5])

                head = Head(text)
                head.addpos(pos)
                head.score = score
                head.occ = occurrence
                head.frequency = frequency
                if proto:
                    head.proto = proto
                self.heads[text] = head
            csvfile.close()
        print("Load ", path,  "  소요시간:" , round(time.time() - starttime, 3))
        
    #########################
    ## Tail 출력 
    #########################
    def writetails(self, path="model/tails.csv", sorter=sortParticle, reversed=False):
        self._write_particles(path, self.tails, False, sorter, reversed)

    
    #########################
    ## Tail 로딩 
    #########################
    def readtails(self, path="model/tails.csv"):
        starttime = time.time()
        with open(path, 'r', encoding='utf-8') as csvfile :
            reader = csv.reader(csvfile)
            for row in reader:
                text = row[0]
                tags = row[1].split('+')
                score = float(row[2])
                occurrence = int(row[3])
                tail = Tail(text)
                tail.addtags(tags)
                tail.score = score
                tail.occ = occurrence
                self.tails[text] = tail
            csvfile.close()
        print("Load ", path,  "  소요시간:" , round(time.time() - starttime, 3))


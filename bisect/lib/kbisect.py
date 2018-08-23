import re
import csv

########################
#  어절 구성 객체 
########################

word_tokenize_pattern = re.compile("[^가-힣a-zA-Z0-9]+")
particle_tokenize_pattern = re.compile("([^가-힣ㄱ-ㅎ]+|[가-힣ㄱ-ㅎ])")


def writecsv(path, datalist, handler):
    with open(path, 'w', encoding='utf-8') as csvfile :
        writer = csv.writer(csvfile)
        for data in datalist:
            handler(writer, data)
        csvfile.close()

def formatPair(csvwriter, pair):
    csvwriter.writerow([pair.head.text, pair.tail.text, pair.score])
    
class Particle:
    def __init__(self,text):
        self.text = text
        self.score = 0.0
        self.occurrence = 0
        self.remains = []
    
    def occur(self):
        self.occurrence += 1
        return self.occurrence
    
    def putremains(self, rem):
        self.remains.append(rem)
            
    
class Pair:
    def __init__(self,head,tail):
        self.head = head
        self.tail = tail
        self.score = 0.0
    
class Word:
    def __init__(self,text):
        self.text = text
        self.pairs = []
        self.bestpair = None
    
    def putpair(self, head,tail):
        self.pairs.append( Pair(head,tail) )
        head.putremains(tail)
        tail.putremains(head)
    
    
    
class Model:
    def __init__(self):
        self.heads = {}
        self.tails = {}
        self.words = {}
        self.maxhead =0
        self.maxtail =0
    
    def word(self, text):
        return self.words.get(text)
    
    def newWord(self, text):
        word = Word(text)
        self.words[text] = word
        return word
        
    def head(self, text):
        return self.heads.get(text)
    
    def puthead(self, text):
        head = self.heads.get(text)
        if not head:
            head = Particle(text)
            self.heads[text] = head
            
        if self.maxhead < head.occur():
            self.maxhead = head.occurrence
        return head
        
    def tail(self,text):
        return self.tails.get(text)
        
    def puttail(self, text):
        tail = self.tails.get(text)
        if not tail:
            tail = Particle(text)
            self.tails[text] = tail
        
        if(len(text)>0):
            if self.maxtail < tail.occur():
                self.maxtail = tail.occurrence
        return tail
        
    
class Bisector():
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.model = Model()
        
    def loadfile(self, path):
        with open(path, 'r', encoding='utf-8') as file :
            lines = file.readlines()
            for row in lines:
                sentences = self.readrow(row)
            file.close()

    def readrow(self, row):
        for word in word_tokenize_pattern.split(row):
            word = word.strip()
            if(len(word)>0):
                self.bisect(word)
    
    def bisect(self, word):
        wordObj = self.model.word(word)
        if wordObj:
            return
        else:
            wordObj = self.model.newWord(word)
        
        tokens = particle_tokenize_pattern.findall(word)
        
        length = len(tokens)
        h,t = None,None
        head,tail = None,None
        
        for index in range(length):
            index += 1
            h = ''.join(tokens[:index])
            head = self.model.puthead(h)
            t = ''.join(tokens[index:])
            tail = self.model.puttail(t)
            wordObj.putpair(head,tail)
    
    def score(self):
        for head in self.model.heads.values():
            self.scoreHead(head)
            
        for tail in self.model.tails.values():
            self.scoreTail(tail)
            
        for word in self.model.words.values():
            bestpair = None
            for pair in word.pairs:
                bestpair = self.scoreWord(pair, bestpair)
            word.bestpair = bestpair
               
    def scoreHead(self, head):
        score = 0
        for rem in head.remains:
            score += rem.occurrence
        
        head.score = float(score / len(head.remains)) * len(head.text) 
        
         
    def scoreTail(self, tail):
        if tail.occurrence == 0:
            tail.score = 0.3
            return
        
        score = 0.0
        for rem in tail.remains:
            score += rem.occurrence
        
        tail.score = float(score / len(tail.remains)) * len(tail.text)
        
          
    def scoreWord(self, pair, bestpair):
        hs = pair.head.score 
        ts = pair.tail.score
        
        pair.score = hs + ts
        
        if bestpair:
            if pair.score >= bestpair.score:
                return pair
            else:
                return bestpair
        else:
            return pair
        
    def writeBestPairs(self, path):
        bestpairs = []
        for word in self.model.words.values():
            bestpairs.append(word.bestpair)
        
        writecsv(path, bestpairs, formatPair )

    
    def writeAllPairs(self, path):
        pairs = []
        for word in self.model.words.values():
            for pair in word.pairs:
                pairs.append(pair)
                
        writecsv(path, pairs, formatPair )

    
import pycor.speechmodel as sm


POS=['S','O','IO', 'P','V','A','AD','C','CL']

auxmap = {}
stemmap = {}
suffixmap = {}
singlemap = {}


def regSng(sw, atag=None):
    if type(sw) is SingleWord or issubclass(type(sw), SingleWord):
        singlemap[sw.text] = sw
        return sw
    elif type(sw) is str:
        swObj = SingleWord(sw, atag)
        singlemap[sw] = swObj
        return swObj


def _putmap1(map, token, worm):
    if len(token) > 1:
        token = token[len(token) -1]
    bag = map.get(token)
    if bag is None:
        bag = []
        map[token] = bag
    bag.append(worm)
    
    return worm

def _putmap2(map, worm):
    for token in worm.tokens:
        _putmap1(map, token, worm)
    return worm

def regAux(worm, atag=None, precedents=None, constraints = None, score=0, escapeFirst=False):
    if type(worm) is Worm or issubclass(type(worm), Worm):
        return _putmap2(auxmap, worm)
        
    elif type(worm) is list:
        wormObj = Aux(worm, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(auxmap, wormObj)
    
    elif type(worm) is str:
        wormObj = Aux(worm, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(auxmap, wormObj)


# 여러 음절의 어미 조사 등록하기 MultiSyllablesAux
def regMultiSyllablesAux(syllables):
    if type(syllables) is not str:
        raise Exception("regMultiSyllablesAux needs string.")
    aux = MultiSyllablesAux(syllables)
    return _putmap2(auxmap, aux)

# list로 반환 
def getAuxs(token):
    return auxmap.get(token)


def regStem(stem, atag=None, precedents=None, constraints = None, score=0, escapeFirst=False):
    if type(stem) is Stem or issubclass(type(stem), Worm):
        return _putmap2(stemmap, stem)
    elif type(stem) is list:
        stemObj = Stem(stem, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(stemmap, stemObj)
    
    elif type(stem) is str:
        stemObj = Stem(stem, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(stemmap, stemObj)

# 여러 음절의 어미 조사 등록하기 MultiSyllablesStem
def regMultiSyllablesStem(syllables, atag=None):
    if type(syllables) is not str:
        raise Exception("regMultiSyllablesStem needs string.")
    stem = MultiSyllablesStem(syllables, atag=atag)
    return _putmap2(stemmap, stem)

# list로 반환 
def getStems(token):
    return stemmap.get(token)


def regSuffix(suffix, atag=None, precedents=None, constraints = None, score=0, escapeFirst=False):
    if type(suffix) is Suffix or issubclass(type(suffix), Worm):
        return _putmap2(suffixmap, suffix)
    elif type(suffix) is list:
        suffixObj = Suffix(suffix, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(suffixmap, suffixObj)
    
    elif type(suffix) is str:
        suffixObj = Suffix(suffix, atag=atag, precedents=precedents, constraints = constraints, score=score, escapeFirst=escapeFirst)
        return _putmap2(suffixmap, suffixObj)

# list로 반환 
def getSuffixes(token):
    return suffixmap.get(token)

class SingleWord:
    def __init__(self, text, atag=None):
        self.text = text
        self.atag = atag

    def tag(self, atag):
        self.atag = atag

WORD_QUOTE_START = regSng("[","QS")
WORD_QUOTE_END = regSng("]","QE")
regSng(".","PT")
regSng("?","QM")
regSng("!","EC")
regSng(":","CL")
regSng(";","SC")
regSng("\n","NL")


class Constraint:
    def __init__(self):
        self.orConsts = []
    
    def Or(self, const):
        self.orConsts.append(const)
        return self
    
    def acceptChain(self, wordTokens, worm, prevWord, nextWord):
        if self.accept(wordTokens, worm, prevWord, nextWord):
            return True
        for orc in self.orConsts:
            if orc.acceptChain(wordTokens, worm, prevWord, nextWord):
                return True

        return False

    def accept(self, wordTokens, worm, prevWord, nextWord):
        return True

class ConstraintOnlyAfter(Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        return prevStr in worm.precedents

class ConstraintAfter(Constraint):
    def __init__(self, prevs):
        super().__init__()
        self.prevs = set(prevs)
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        return prevStr in self.prevs


class ConstraintCollocation(Constraint):
    def __init__(self, prevWordEnd=None, nextWordFirst=None):
        super().__init__()
        self.prevWordEnd = prevWordEnd
        self.nextWordFirst = nextWordFirst

    def accept(self, wordTokens, worm, prevWord, nextWord):
        # print("self.prevWordEnd", self.prevWordEnd, "self.nextWordFirst", self.nextWordFirst, "nextWord", nextWord)
        if self.prevWordEnd :
            if not prevWord or not prevWord.endswith(self.prevWordEnd):
                return False
        # print("prevWordEnd pass" )
        if self.nextWordFirst:
            if not nextWord or not nextWord.startswith(self.nextWordFirst):
                return False
        # print("nextWordFirst pass" )

        return True


onlyAfter = ConstraintOnlyAfter()

############################################
# 조사, 어미, 접미사 
############################################
class Worm:
    def __init__(self, tokens, atag=None, precedents = None, constraints = [], 
        score=0, escapeFirst=True, ambi=False, pos=None):
        self._set( tokens, atag, precedents , constraints , score, escapeFirst,ambi,pos )
        
    def _set(self, tokens, atag=None, precedents = None, constraints = [], 
        score=0, escapeFirst=True, ambi=False, pos=None):
        self.tokens = set(tokens)
        self.score = score
        self.escapeFirst = escapeFirst
        self.atag = atag
        self.ambi = ambi
        self.pos = pos
        
        self.constraints = []
        if constraints:
            for const in constraints:
                self.addConst(const)
                
        self.precedents = {}
        if precedents:
            for pre in precedents:
                if type(pre) is list:
                    self.addPres(pre)
                else:
                    self.addPre(pre)
                
    def tag(self, tag):
        self.atag = tag
        return self
    
    def setscore(self, score):
        self.score = score
        return self
    
    def setpos(self, pos):
        self.pos = pos
        return self
    
    def isAmbi(self):
        return self.ambi
    
    def ambiguous(self, ambi=True):
        self.ambi = ambi
        return self
    
    def incase(self, constraints):
        self.addConst(constraints)
        return self
    
    def after(self, worms):
        if type(worms) is list:
            self.addPres(worms)
        else:
            self.addPre(worms)
        return self
    
    def afterWords(self, words):
        aux = makeMultiSyllablesAux(words)
        self.after(aux)
        return self
    
    
    def addPre(self, worm):
        for t in worm.tokens:
            bag = self.precedents.get(t)
            if bag is None:
                bag = []
                self.precedents[t] = bag
            bag.append(worm)
        return self
    
    def addPres(self, worms):
        for worm in worms:
            if type(worm) is list:
                self.addPres(worm)
            else:
                self.addPre(worm)
        return self
    
    def addConst(self, const):
        if type(const) is list:
            self.constraints.extend(const)
        else:
            self.constraints.append(const)
        return self
    
    def getPrecedent(self, wordTokens, lastPair):
        pre = wordTokens.peekPrev()
        return self.precedents.get(pre)
    
    def isOnlyAfter(self):
        return onlyAfter in self.constraints
    
    def _checkConstraints(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        if wordTokens.peekPrev() is None and self.escapeFirst:
            return False
        
        if self.constraints:
            for const in self.constraints:
                #print("procede ", wordTokens.text, wordTokens.current())
                if not const.acceptChain(wordTokens, self, prevWord, nextWord) :
                    #print('  ', wordTokens.current(), "NO")
                    return False
        return True

    def procede(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord ):
        if not self._checkConstraints(wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord) :
            return None
        
        headtails = []
        
        headtail = self._procedeImpl( wordTokens, followingWorm, wordObj, prevPair , prevWord , nextWord )
        

        if headtail:
            headtails.append( headtail )
            headtail.ambiguous(self.ambi)
            
            # if headtail.score < 0 and wordTokens.fromEnd() <= 1:
            #     ht = sm.Pair(wordTokens.text, None, self.score, self.atag, self.ambi )
            #     headtails.append( ht )
            
        if wordTokens.peekPrev() :
            lastPair = headtail if headtail else prevPair
            upWorms = self.getUpWorms(wordTokens, self, wordObj, lastPair, prevWord, nextWord)
            if upWorms:
                curidx = wordTokens.curidx;
                for upWorm in upWorms:
                    hts = upWorm.procede(wordTokens, self, wordObj, lastPair , prevWord, nextWord)
                    if hts:
                        headtails.extend( hts )
                    wordTokens.setPos(curidx)
            
        lastPair = headtails[len(headtails)-1] if len(headtails)> 0 else prevPair
        preWorms = self.getPrecedent(wordTokens, lastPair)
        
        if preWorms :
            curidx = wordTokens.curidx;
            for preWorm in preWorms:
                wordTokens.prev()
                hts = preWorm.procede(wordTokens, self, wordObj, lastPair , prevWord, nextWord)
                if hts:
                    headtails.extend( hts )
                wordTokens.setPos(curidx)
            
        return headtails

    def getTag(self,prevPair) :
        tags = []
        if prevPair:
            tags.extend(prevPair.tags)
        if self.atag:
            tags.append(self.atag)
        return tags
        # return (self.atag if self.atag else '') + ( "+" + prevPair.type if prevPair and prevPair.type else '')

    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        return sm.Pair(wordTokens.head(), wordTokens.tail(), self.score).addpos(self.pos).addtags(self.getTag(prevPair))

    def getUpWorms(self,wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        return None


class _MultiSyllablesWorm(Worm) :
    def _set(self, syllables, atag=None, precedents = None, constraints = [], 
        score=0, escapeFirst=False, ambi=False, pos=None):
        first, last = self.makeInnerWorm(syllables)
        # 첫음절 
        self.first = first
        # 마지막 음절 
        self.last = last
        self.tokens = set(syllables[len(syllables)-1])
        self.syllables = syllables
        self.first.score = score
        self.first.escapeFirst = escapeFirst
        self.first.atag = atag
        self.first.ambi = ambi
        self.atag = atag
        
        if constraints:
            for const in constraints:
                self.first.addConst(const)
                
        if precedents:
            for pre in precedents:
                if type(pre) is list:
                    self.first.addPres(pre)
                else:
                    self.first.addPre(pre)
                
    def makeInnerWorm(self, syllables):
        raise Exception("_MultiSyllablesWorm makeInnerWorm to be implemented")
    
    def tag(self, tag):
        self.atag = tag
        self.first.atag = tag
        return self
    
    def setscore(self, score):
        self.first.score = score
        return self
    
    def isAmbi(self):
        return self.first.ambi
    
    def ambiguous(self, ambi=True):
        self.first.ambi = ambi
        return self
    
    def incase(self, constraints):
        self.first.addConst(constraints)
        return self
    
    def after(self, worms):
        self.first.after(worms)
        return self
    
    def addPre(self, worm):
        self.first.addPre(worm)
        return self
    
    def addPres(self, worms):
        self.first.addPres(worms)
        return self
    
    def addConst(self, const):
        self.first.addConst(const)
        return self
    
    def isOnlyAfter(self):
        return self.first.isOnlyAfter()
    
    def getPrecedent(self, wordTokens, lastPair):
        raise Exception("_MultiSyllablesWorm cannot getPrecedent")
    
    # Consume tokens to Last
    def _checkConstraints(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        fromIdx = wordTokens.curidx - len(self.syllables)+1
        if fromIdx < 0:
            return False
        
        text = ''.join(wordTokens.current(fromIdx))
        #print(self.syllables, text)
        if text != self.syllables:
            return False

        wordTokens.setPos(fromIdx)

        return self.first._checkConstraints(wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord)

    def procede(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord ):
        if not self._checkConstraints(wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord) :
            return None
        # 마지막 음절까지 이동한 상태 
        return self.first.procede(wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord)

    def getTag(self,prevPair) :
        return (self.first.atag if self.first.atag else '') + ( "+" + prevPair.type if prevPair and prevPair.type else '')

    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        raise Exception("_MultiSyllablesWorm cannot _procedeImpl")

    def getUpWorms(self,wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        raise Exception("_MultiSyllablesWorm cannot getUpWorms")


############################################
# 조사, 어미, 접미사 
############################################
class Aux(Worm):
    def __init__(self, tokens, atag=None, precedents = None, constraints = [], 
        score=0, escapeFirst=True, ambi=False, pos=None):
        super().__init__( tokens, atag, precedents , constraints , score, escapeFirst,ambi,pos )
        
    def __repr__(self):
        return "Aux["+ ','.join(str(s) for s in self.tokens) +"] " + str(self.atag)
    
    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        if not self.isOnlyAfter():
            return sm.Pair(wordTokens.head(), wordTokens.tail(), self.score).addtags(self.getTag(prevPair))

    def getUpWorms(self,wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        token = None
        if prevPair and prevPair.head :
            token = prevPair.head[len(prevPair.head) -1]
        else :
            token = wordTokens.peekPrev()
        
        return getStems(token)


class MultiSyllablesAux(_MultiSyllablesWorm) :
    def __repr__(self):
        return "MultiSyllablesAux["+ self.syllables +"] " + str(self.atag)
    
    def makeInnerWorm(self, syllables):
        first = Aux(syllables[0])
        last = Aux(syllables[len(syllables)-1])
        last.after(first)
        return first , last
    
    def getUpWorms(self,wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        token = None
        if prevPair and prevPair.head :
            token = prevPair.head[len(prevPair.head) -1]
        else :
            token = wordTokens.peekPrev()
        return getStems(token)

    
############################################
# Stem 어간 
############################################
class Stem(Worm):
    def __init__(self, tokens, atag=None, precedents=None, constraints = None, 
        score=0, escapeFirst=False, ambi=False, pos=None):
        super().__init__( tokens, atag, precedents , constraints , score, escapeFirst,ambi,pos )
    
    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        idx = wordTokens.curidx
        return sm.Pair(wordTokens.head(idx), wordTokens.tail(idx), self.score+1).addtags(self.getTag(prevPair)).addpos(self.pos)

class MultiSyllablesStem(_MultiSyllablesWorm) :
    def __repr__(self):
        return "MultiSyllablesStem["+ self.syllables +"] " + str(self.atag)
    
    def makeInnerWorm(self, syllables):
        first = Stem(syllables[0])
        last = Stem(syllables[len(syllables)-1])
        last.after(first)
        return first , last

# 체언 단독 어절로 쓰일 경우 형태 보존을 위한 Aux 
class StemAux(_MultiSyllablesWorm):
    def __repr__(self):
        return "StemAux["+ self.syllables +"] " + str(self.atag)
    
    def escape(self, escps):
        self.first.escape(escps)
        return self

    def makeInnerWorm(self, syllables):
        first = _InnerStemAux(syllables[0], len(syllables))
        last = Aux(syllables[len(syllables)-1])
        last.after(first)
        return first , last

# 체언 단독 어절로 쓰일 경우 형태 보존을 위한 Aux 
class _InnerStemAux(Worm):
    def __init__(self, tokens, length, atag=None, precedents=None, constraints = None, 
        score=0, escapeFirst=False, ambi=False, pos=None):
        super().__init__( tokens, atag, precedents , constraints , score, escapeFirst,ambi,pos )
        self.length = length
        self.excape = []
    
    def escape(self, escps):
        if type(escps) is list:
            self.excape.extend(escps)
        else:
            self.excape.append(escps)
        return self

    def _checkConstraints(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        if wordTokens.peekPrev() is None and self.escapeFirst:
            return False
        elif (wordTokens.head() in self.excape):
            return False
                
        if self.constraints:
            for const in self.constraints:
                #print("procede ", wordTokens.text, wordTokens.current())
                if not const.acceptChain(wordTokens, self, prevWord, nextWord) :
                    #print('  ', wordTokens.current(), "NO")
                    return False
        return True
        
    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        idx = wordTokens.curidx + self.length
        return sm.Pair(wordTokens.head(idx), wordTokens.tail(idx), self.score).addtags(self.getTag(prevPair)).addpos(self.pos)

    
############################################
# 접미사  
############################################
class Suffix(Worm):
    def __init__(self, tokens, atag=None, precedents=None, constraints = None, 
        score=0, escapeFirst=True, ambi=False, pos=None):
        super().__init__( tokens, atag, precedents , constraints , score, escapeFirst,ambi,pos )

    def _procedeImpl(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        head = wordTokens.head()
        tail = wordTokens.tail()

        return sm.Pair(head, tail, self.score+1).addpos(self.pos)


    
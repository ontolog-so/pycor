import sys
import pycor.langmodel as lm
import pycor.speechmodel as sm
import pycor.korutils as korutils


def buildJongsungAux(jongsung):
    if jongsung in korutils.phoneme_final:
        tokens = []
        for cho in korutils.phoneme_first:
            for jung in korutils.phoneme_vow:
                ch = korutils.compose(cho, jung, jongsung)
                tokens.append(ch)

        return JongsungAux(tokens, jongsungs=jongsung) 

def buildWithJongsungAux(jongsung):
    if jongsung in korutils.phoneme_final:
        tokens = []
        for cho in korutils.phoneme_first:
            for jung in korutils.phoneme_vow:
                ch = korutils.compose(cho, jung, jongsung)
                tokens.append(ch)

        return WithJongsungAux(tokens, jongsungs=jongsung) 

##################################################
# Constraint 세팅 
##################################################
class ConstraintAfterJongsung(lm.Constraint):
    def __init__(self, jongsungs=[]):
        super().__init__()
        self.jongsungs = set(jongsungs)
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            if(len(self.jongsungs)>0):
                return final in self.jongsungs
            else:
                return len(final) > 0
        else:
            return True
        
class ConstraintWithJongsung(lm.Constraint):
    def __init__(self, jongsungs):
        super().__init__()
        self.jongsungs = set(jongsungs)
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        curStr = wordTokens.current()
        if korutils.isKor(curStr):
            first,vowel,final = korutils.decompose(curStr)
            return final in self.jongsungs
        else:
            return False
        
class ConstraintAfterVowel(lm.Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            #print("*****", wordTokens.text, wordTokens.current(), final, len(final), len(final) == 0)
            return len(final) == 0
        else:
            return True

class ConstraintAfterPositiveVowel(lm.Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            #print("*****", wordTokens.text, wordTokens.current(), final, len(final), len(final) == 0)
            return vowel in korutils.POSITIVE_VOWEL
        else:
            return False

class ConstraintAfterNegativeVowel(lm.Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            #print("*****", wordTokens.text, wordTokens.current(), final, len(final), len(final) == 0)
            return vowel in korutils.NEGATIVE_VOWEL
        else:
            return False

class ConstraintAfterVowelOrJongsung(lm.Constraint):
    def __init__(self, jongsungs):
        super().__init__()
        self.jongsungs = set(jongsungs)

    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            #print("*****", wordTokens.text, wordTokens.current(), final, len(final), len(final) == 0)
            return len(final) == 0 or final in self.jongsungs
        else:
            return True


class ConstraintFinal(lm.Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        return wordTokens.peekNext() is None


class ConstraintAfter(lm.Constraint):
    def __init__(self, prevs):
        super().__init__()
        self.prevs = set(prevs)
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        return ( prevStr in self.prevs )

class ConstraintMoreThanAfter(lm.Constraint):
    def __init__(self, prevCount):
        super().__init__()
        self.prevCount = prevCount
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        return ( wordTokens.curidx > self.prevCount )

class ConstraintLessThanAfter(lm.Constraint):
    def __init__(self, prevCount):
        super().__init__()
        self.prevCount = prevCount
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        return ( wordTokens.curidx < self.prevCount )


class ConstraintNotAfter(lm.Constraint):
    def __init__(self, prevs):
        super().__init__()
        self.prevs = set(prevs)
        
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        return not( prevStr in self.prevs )


# 첫 음절인 경우에만 
class ConstraintFirst(lm.Constraint):
    def accept(self, wordTokens, worm, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        #print("ConstraintFirst ", wordTokens.current(), prevStr, wordTokens.tail())
        return prevStr is None

##################################################
# Aux 확장  
##################################################
# 종성 어미 뒤에 오는 어미 
class WithJongsungAux(lm.Aux) :
    def __init__(self, tokens, jongsungs,  atag=None, precedents = None, constraints = [], score=0, escapeFirst=True, ambi=False):
        self._set( tokens, atag, precedents , constraints , score, escapeFirst,ambi )
        self.constraints.append(ConstraintAfterJongsung(jongsungs))
        self.jongsungs = jongsungs
        
    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        prevStr = wordTokens.peekPrev()
        #print("#### NextJongsungAux ** ", prevStr)
        if korutils.isKor(prevStr):
            first,vowel,final = korutils.decompose(prevStr)
            #print("***NextJongsungAux **", prevStr, final , final in self.jongsungs)
            if final in self.jongsungs :
                removed = korutils.removeJongsung(prevStr)
                head = ''.join([wordTokens.head(wordTokens.curidx-1), removed])
                tail = ''.join([final, wordTokens.tail()])
                return sm.Pair(head, tail, self.score).addtags(self.getTag(prevPair))     
        return None
    
# 종성 어미  
class JongsungAux(lm.Aux) :
    def __init__(self, tokens, jongsungs,  atag=None, precedents = None, constraints = [], score=0, escapeFirst=True, ambi=False):
        self._set( tokens, atag, precedents , constraints , score, escapeFirst,ambi )
        self.constraints.append(ConstraintWithJongsung(jongsungs))
        self.jongsungs = jongsungs
        
    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        curStr = wordTokens.current()
        if korutils.isKor(curStr):
            first,vowel,final = korutils.decompose(curStr)
            
            if final in self.jongsungs :
                removed = korutils.removeJongsung(curStr)
                head = ''.join([wordTokens.head(wordTokens.curidx), removed])
                tail = ''.join([final, wordTokens.tail(wordTokens.curidx+1)])
                return sm.Pair(head, tail, self.score).addtags(self.getTag(prevPair)) 
        
        return None


# 여러 글자의 어미 
class MultiCharsAux(lm.Aux) :
    def __init__(self, chars,  atag=None, precedents = None, constraints = [], score=0, escapeFirst=True, ambi=False):
        self._set( chars[0], atag, precedents , constraints , score, escapeFirst,ambi )
        self.chars = chars

    def _doConstraints(self, wordTokens, followingWorm, wordObj, prevPair, prevWord, nextWord):
        gap = len(self.chars) - 1
        toIdx = wordTokens.curidx - gap
        chars = wordTokens.current(toIdx)
        return chars == self.chars

    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        gap = len(self.chars) - 1
        toIdx = wordTokens.curidx - gap
        wordTokens.setPos(toIdx)

        return sm.Pair(wordTokens.head(), wordTokens.tail(), self.score).addtags(self.getTag(prevPair)) 
    

#############################
# Aux 어간의 형태를 바꾸는 어미 
#############################
class TransformedAux(lm.Aux) :
    def __init__(self, tokens, head, tail,  atag=None, precedents = None, constraints = [], score=0, escapeFirst=True, ambi=False):
        self._set( tokens, atag, precedents  , constraints , score, escapeFirst,ambi )
        self.head = head
        self.tail = tail
        
    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        curStr = wordTokens.current()
        #print("TransformedAux", curStr)
        if korutils.isKor(curStr):
            head = ''.join([wordTokens.head(wordTokens.curidx), self.head])
            tail = ''.join([self.tail, wordTokens.tail(wordTokens.curidx+1)])
            #print("TransformedAux2 head=", head, ", tail=", tail)
            return sm.Pair(head, tail, self.score).addtags(self.getTag(prevPair)) 
        return None

#############################
# 불규칙 활용 어미 
#############################
class IrregularAux(lm.Aux) :
    def __init__(self, tokens, headJongsung, tail,  atag=None, precedents = None, constraints = [], score=0, escapeFirst=True, ambi=False):
        self._set( tokens, atag, precedents  , constraints , score, escapeFirst,ambi )
        self.headJongsung = headJongsung
        self.tail = tail
        
    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        curStr = wordTokens.current()
        prevStr = wordTokens.peekPrev()

        if korutils.isKor(curStr):
            prevStr = korutils.addJongsung(prevStr, self.headJongsung)
            head = ''.join([wordTokens.head(wordTokens.curidx-1), prevStr])
            tail = ''.join([self.tail, wordTokens.tail(wordTokens.curidx+1)])
            return sm.Pair(head, tail, self.score).addtags(self.getTag(prevPair))    
        return None

#############################
# Stem   형태가 바뀌는 어간 
#############################
class TransformedStem(lm.Stem) :
    def __init__(self, tokens, head, atag=None, precedents = None, constraints = [], score=0, escapeFirst=False, ambi=False):
        self._set( tokens, atag, precedents  , constraints , score, escapeFirst,ambi )
        self.head = head
        
    def _procedeImpl(self,wordTokens, followingAux, wordObj, prevPair, prevWord, nextWord):
        #print("TransformedStem", self.head)
        curStr = wordTokens.current()
        if korutils.isKor(curStr):
            head = ''.join([wordTokens.head(wordTokens.curidx), self.head])
            tail = wordTokens.tail(wordTokens.curidx+1)
            return sm.Pair(head, tail, self.score).addtags(self.getTag(prevPair)).addpos(self.pos)      
        return None

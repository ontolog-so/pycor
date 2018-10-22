#####################################################################
# 
#   통사체 Syntagme 처리 
# 
#####################################################################
import pycor.speechmodel as sm

syntagms = []

def regSyntagm(syntagm):
    syntagms.append(syntagm)
    return syntagm

def processSyntagms(syntagmCursor, documentContext, index=None):
    if index is None:
        index = syntagmCursor.curidx

    curWord = syntagmCursor.current()

    if issubclass(type(curWord), sm.WordGroup):
        _processSyntagmsSub(curWord,documentContext)
    else:
        for syntagm in syntagms:
            syntagmCursor.setPos(index)
            if syntagm.accept(curWord, documentContext):
                syntagm.process(syntagmCursor, documentContext)

def _processSyntagmsSub(wordgroup, documentContext):
    syntagmCursor = SyntagmCursor()
    syntagmCursor.set(wordgroup)
    syntagmCursor.toEnd()
    processSyntagms(syntagmCursor,documentContext)


##################################################
#  문장 단위 어절 커서  
##################################################
class SyntagmCursor :
    def set(self,sentence):
        self.sentence = sentence
        self.curidx = None
        self.length = len(sentence.words)

    def setPos(self, index):
        self.curidx = index
        return self
    
    def toStart(self):
        self.curidx = 0
        return self.current()
        
    def toEnd(self):
        self.curidx = self.length -1
        return self.current()
        
    def current(self, toIdx=None):
        if toIdx is None:
            return self.sentence.words[self.curidx]
        else :
            if toIdx > self.curidx:
                return self.sentence.words[self.curidx:toIdx]
            else:
                return self.sentence.words[toIdx:self.curidx+1]

    def currentPair(self, toIdx=None):
        if toIdx is None:
            return self.sentence.pairs[self.curidx]
        else :
            if toIdx > self.curidx:
                return self.sentence.pairs[self.curidx:toIdx]
            else:
                return self.sentence.pairs[toIdx:self.curidx+1]

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
        
    def nextPair(self, size=1):
        if self.curidx is None:
            self.curidx = -1
        
        if self.curidx < self.length-1:
            self.curidx += 1
            if size > 1:
                nextpos = self.curidx + size 
                tokens = self.sentence.pairs[self.curidx:nextpos]
                self.curidx = nextpos-1
                return tokens
            else:
                return self.sentence.pairs[self.curidx]
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
    
    def prevPair(self, size=1):
        if self.curidx is None:
            self.curidx = self.length
        
        if self.curidx > 0:
            if size > 1:
                prevpos = self.curidx - size
                tokens = self.sentence.pairs[prevpos:self.curidx]
                self.curidx = prevpos
                return tokens
            else:
                self.curidx -= 1
                return self.sentence.pairs[self.curidx]
        else :
            return None


##################################################
#  Syntagm Filter
##################################################
class Filter:
    def accept(self, curWord, documentContext):
        return False

class PosFilter(Filter):
    def __init__(self, pos):
        self.pos = set()
        if type(pos) is list:
            self.pos.update(pos)
        else:
            self.pos.add(pos)

    def accept(self, curWord, documentContext):
        return len(self.pos & curWord.bestpair.pos) > 0
    
class TagFilter(Filter):
    def __init__(self, tags):
        self.tags = set()
        if type(tags) is list:
            self.tags.update(tags)
        else:
            self.tags.add(tags)

    def accept(self, curWord, documentContext):
        return len(self.tags & set(curWord.bestpair.tags)) > 0
    
##################################################
#  Syntagm
##################################################
class Syntagm :
    def __init__(self):
        self.filters = []

    def incase(self, filters):
        if type(filters) is list:
            self.filters.extend(filters)
        else:
            self.filters.append(filters)
        return self
    
    def accept(self, curWord, documentContext):
        if self.filters:
            for filter in self.filters:
                if not filter.accept(curWord, documentContext) :
                    return False
        return True
    
    def process(self, syntagmCursor, documentContext):
        pass

class PTSyntagm(Syntagm) :
    def __init__(self):
        super().__init__()
        self.handlers = {}
        self.incase(PosFilter("PT"))

    def addHandler(self, lastTag, handler):
        self.handlers[lastTag] = handler
        return self

    def process(self, syntagmCursor, documentContext):
        last = syntagmCursor.prev()
        if last is None:
            return
            
        if issubclass(type(last), sm.WordGroup):
            _processSyntagmsSub(last, documentContext)
        else:
            lastpair = last.bestpair
            tags = lastpair.tags
            index = syntagmCursor.curidx
            for key, handler in self.handlers.items():
                syntagmCursor.setPos(index)
                if key in tags:
                    handler(lastpair, syntagmCursor, documentContext)

# PTSyntagm 객체 
ptSyntagm = regSyntagm( PTSyntagm() )
import re
from threading import Lock
from pycor import korutils, parser
from pycor import morpheme as lm
from pycor import speechmodel as sm


# Y_TAGS0 = set(['EFN','ETN','EFQ'])
# Y_TAGS1 = set(['EPT-pp','EPT-f','EPT-guess','EFN','EFI','EC-to','EC-for','EC-but'])
# Y_TAGS2 = set(['EPT-pr','ETM'])

# C_TAGS0 = set(['JKS','JKC','JKP'])
# C_TAGS1 = set(['JKG','JKB-TO','JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY',
#                 'EC-evenif','JKG-as','JKB-CM'])
# C_TAGS2 = set(['JKO','JX-SO'])
# C_POS = set(['NP','NNB'])

def _debug_word(writer, word):
    if len(word.particles) == 0:
        writer.writerow([word.text, 'X'])
    for part in word.particles:
        h = part.head.text if part.head else ''
        t = part.tail.text if part.tail else ''
        writer.writerow([word.text, h, t, part.score, part.tags, part.pos])


class Trainer(parser.SentenceParser) :
    def __init__(self, wordsthreshold=100000):
        super().__init__()
        self.wordsthreshold = wordsthreshold
        print("Init Trainer")
        self.lock = Lock()

    def setwordlimit(self, wordsthreshold):
        self.wordsthreshold = wordsthreshold

    def buildVocab(self, debugWriter=None) :
        if len(self.wordmap.words) < 3:
            return

        for word in self.wordmap.words.values():
            self.scoreword(word, force=True)
        
        collList = list(self.wordmap.collocations.values())

        for col in collList:
            if col.frequency < 3:
                del self.wordmap.collocations[col.text]
                
        snglist, ylist, clist, ambilist = self.classifyWords(self.wordmap.words.values())

        print("Single Count:", len(snglist))
        print("용언 Count:", len(ylist))
        print("체언 Count:", len(clist))
        print("Ambiguous Count:", len(ambilist))
        print("Heads Count:", len(self.wordmap.heads))
        print("Collocations Count:", len(self.wordmap.collocations))
        print("Tails Count:", len(self.wordmap.tails))

        if debugWriter:
            debugWriter.writerow(["---",len(self.wordmap.words),"---"])
            for word in self.wordmap.words.values():
                _debug_word(debugWriter, word)
            
        self.wordmap.clearwords()

        return snglist, ylist, clist, ambilist
    
    def train(self,filepath, debugWriter=None):
        sentence_array = self.loadfile(filepath)
        # self._doresolver(sentence_array)
        self.checkVocab(sentence_array, debugWriter)

    # 각 문서별 Scoring 생략 
    # def resolveDocument(self, sentence_array):
    #     return None
 

    def checkVocab(self, sentence_array, debugWriter=None):
        if len(self.wordmap.words) > self.wordsthreshold :
            self.buildVocab(debugWriter)
        return None
        

    def classifyWords(self,words):
        headTagsMap = {}
        for word in words:
            if word.bestpair:
                head = word.bestpair.head
                tail = word.bestpair.tail
                tags = headTagsMap.get(head)
                if not tags:
                    tags = set()
                    headTagsMap[head] = tags

                tags.update(tail.tags)

        # tuples = list(headTagsMap.items())
        # for head, tags in  tuples:
        #     self.analyzeHead(head, tags, self.wordmap.heads, headTagsMap)

        snglist = []
        ylist = []
        clist = []
        ambilist = []
        for head, tags in  headTagsMap.items():
            self.classify(head, tags, snglist, ylist, clist, ambilist)

        return snglist, ylist, clist, ambilist

    # def analyzeHead(self,head, tags, headMap, headTagsMap):
    #     headText = head.text
    #     length = len(headText)

    #     if length < 2:
    #         return
            
    #     suffixes = lm.getSuffixes(headText[length-1])
        
    #     if suffixes:
    #         wordTokens = parser.WordTokens(headText)
    #         wordTokens.prev()
    #         curindex = wordTokens.curidx
    #         for suf in suffixes:
    #             wordTokens.setPos(curindex)
    #             pairs = suf.procede(wordTokens,None,None,None,None,None,head, tags)

    def classify(self,head, tags, snglist, ylist, clist, ambilist):
        if 'Y' in head.pos:
            ylist.append(head)
        if 'C' in head.pos:
            clist.append(head)
        if 'SNG' in head.pos:
            snglist.append(head)
        if 'AMBI' in head.pos:
            ambilist.append(head)
        
    # def classifyAmbi(self,head, tags, snglist, ylist, clist, ambilist):
    #     yscore = 0.0
    #     cscore = 0.0

    #     for tail in head.tails:
    #         yscore += len(Y_TAGS0 & tail.tags) * 3
    #         yscore += len(Y_TAGS1 & tail.tags) * 2
    #         yscore += len(Y_TAGS2 & tail.tags) 

    #         cscore += len(C_TAGS1 & tail.tags) * 3
    #         cscore += len(C_TAGS2 & tail.tags) * 2

    #         if max(yscore,cscore) > 0 and abs(yscore-cscore) / max(yscore,cscore) < 0.3:
    #             # print(head.text, abs(yscore-cscore), max(yscore,cscore))
    #             head.addpos('AMBI')
    #             ambilist.append(head)
    #         elif yscore > cscore:
    #             head.addpos('Y')
    #             ylist.append(head)
    #         elif cscore > yscore :
    #             if len(head.pos) > 0 and (head.pos & C_POS) == 0:
    #                 snglist.append(head)
    #             else:
    #                 head.addpos('C')
    #                 clist.append(head)
    #         else:
    #             head.addpos('AMBI')
    #             ambilist.append(head)

    



import re
from threading import Lock
from pycor import korutils, parser
from pycor import langmodel as lm
from pycor import speechmodel as sm


Y_TAGS0 = set(['EFN','ETN','EFQ'])
Y_TAGS1 = set(['EPT-pp','EPT-f','EPT-guess','EFN','EFI','EC-and','EC-to','EC-for','EC-but'])
Y_TAGS2 = set(['EPT-pr','ETM'])

C_TAGS1 = set(['JKS','JKP','JKC','JKG','JKB-TO','JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY',
                'EC-evenif','JKG-as','JKB-CM'])
C_TAGS2 = set(['JKO','JX-SO'])
C_POS = set(['NP','NNB'])


class Trainer(parser.SentenceParser) :
    def __init__(self, wordsthreshold=100000):
        super().__init__()
        self.wordsthreshold = wordsthreshold
        self.checkCount = 1
        print("Init Trainer")
        self.lock = Lock()

    def setwordlimit(self, wordsthreshold):
        self.wordsthreshold = wordsthreshold

    def buildVocab(self) :
        if len(self.wordmap.words) < 3:
            return

        for word in self.wordmap.words.values():
            self.scoreword(word)
        
        snglist, ylist, clist, ambilist = self.classifyHeads(self.wordmap.words.values())

        print("Single Count:", len(snglist))
        print("용언 Count:", len(ylist))
        print("체언 Count:", len(clist))
        print("Ambiguous Count:", len(ambilist))
        print("Heads Count:", len(self.wordmap.heads))
        print("Tails Count:", len(self.wordmap.tails))

        self.wordmap.clearwords()

        return snglist, ylist, clist, ambilist
    
    def train(self,filepath):
        sentence_array = self._loadfile(filepath)
        self.checkVocab(sentence_array)


    def checkVocab(self, sentence_array):
        if len(self.wordmap.words) > self.wordsthreshold * self.checkCount:
            self.checkCount += 1
            self.buildVocab()
        return None
        

    def classifyHeads(self,words):
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

        tuples = list(headTagsMap.items())
        for head, tags in  tuples:
            self.analyzeHead(head, tags, self.wordmap.heads, headTagsMap)

        snglist = []
        ylist = []
        clist = []
        ambilist = []
        for head, tags in  headTagsMap.items():
            self.classify(head, tags, snglist, ylist, clist, ambilist)

        return snglist, ylist, clist, ambilist

    def analyzeHead(self,head, tags,headMap, headTagsMap):
        headText = head.text
        length = len(headText)

        if length < 2:
            return
            
        suffixes = lm.getSuffixes(headText[length-1])
        
        if suffixes:
            wordTokens = parser.WordTokens(headText)
            wordTokens.prev()
            curindex = wordTokens.curidx
            for suf in suffixes:
                wordTokens.setPos(curindex)
                pairs = suf.procede(wordTokens,None,None,None,None,None)
                if pairs:
                    for pair in pairs:
                        stemHead = headMap.get( pair.head )
                        if stemHead is None:
                            stemHead = sm.Head(pair.head)
                            headMap[pair.head] = stemHead

                        # stemHead.addpos()
                        if stemHead.score == 0:
                            stemHead.score = head.score

                        stemHead.occ += head.occ
                        headTagsMap[stemHead] = set()
                        head.proto = pair.head
                        head.addpos(pair.pos)

    # def _analyzeHeadText(self,headText, headMap, headTagsMap, tempHeadBag):
    #     for index in range(1,len(headText)):
    #         left = headText[:index]
    #         right = headText[index:]
    #         leftHead = headMap.get(left)
    #         rightHead = headMap.get(right)
    #         if leftHead:
    #             tempHeadBag[left] = leftHead

    #         if rightHead:
    #             tempHeadBag[right] = rightHead
    #         # else :
    #         #     self._analyzeHeadText(right, headMap, headTagsMap, tempHeadBag)

    def classify(self,head, tags, snglist, ylist, clist, ambilist):
        if len(head.tails) == 0:
            snglist.append(head)

            if len(head.pos) == 0:
                head.addpos('SNG')
        else:
            if len(head.tails) == 0:
                ambilist.append(head)
            
            yscore = len(tags & Y_TAGS0) * 4 + len(tags & Y_TAGS1) * 3 + len(tags & Y_TAGS2) * 1
            cscore = len(tags & C_TAGS1) * 3 + len(tags & C_TAGS2) * 2
            
            if len(head.pos) == 0:
                if yscore > cscore:
                    # print("Y:", head.text, yscore)
                    head.addpos('Y')
                    ylist.append(head)
                elif cscore > yscore:
                    # print("C:", head.text, cscore)
                    head.addpos('C')
                    clist.append(head)
                else:
                    # print("Ambiguous:", head.text, tags, yscore, cscore, head.tails)
                    head.addpos('AMBI')
                    ambilist.append(head)
                    # classifyAmbi(head, tags, snglist, ylist, clist, ambilist)
        
    def classifyAmbi(self,head, tags, snglist, ylist, clist, ambilist):
        yscore = 0.0
        cscore = 0.0

        for tail in head.tails:
            yscore += len(Y_TAGS0 & tail.tags) * 3
            yscore += len(Y_TAGS1 & tail.tags) * 2
            yscore += len(Y_TAGS2 & tail.tags) 

            cscore += len(C_TAGS1 & tail.tags) * 3
            cscore += len(C_TAGS2 & tail.tags) * 2

            if max(yscore,cscore) > 0 and abs(yscore-cscore) / max(yscore,cscore) < 0.3:
                # print(head.text, abs(yscore-cscore), max(yscore,cscore))
                head.addpos('AMBI')
                ambilist.append(head)
            elif yscore > cscore:
                head.addpos('Y')
                ylist.append(head)
            elif cscore > yscore :
                if len(head.pos) > 0 and (head.pos & C_POS) == 0:
                    snglist.append(head)
                else:
                    head.addpos('C')
                    clist.append(head)
            else:
                head.addpos('AMBI')
                ambilist.append(head)

    



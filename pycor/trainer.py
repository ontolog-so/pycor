import re
from threading import Lock
from pycor import speechmodel , korutils, parser


Y_TAGS0 = set(['EFN','ETN'])
Y_TAGS1 = set(['EPT-pp','EPT-f','EPT-guess','EFN','EFI','EC-and','EC-to','EC-for'])
Y_TAGS2 = set(['EPT-pr','ETM'])

C_TAGS1 = set(['JKS','JKP','JKC','JKG','JKB-TO','JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY',
                'EC-evenif','JKG-as','JKB-CM'])
C_TAGS2 = set(['JKO','JX-SO'])
C_POS = set(['NP','NNB'])

def classifyHeads(words):
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

    snglist = []
    ylist = []
    clist = []
    ambilist = []
    for head, tags in  headTagsMap.items():
        classify(head, tags, snglist, ylist, clist, ambilist)

    return snglist, ylist, clist, ambilist

def classify(head, tags, snglist, ylist, clist, ambilist):
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
    
def classifyAmbi(head, tags, snglist, ylist, clist, ambilist):
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


class Trainer(parser.SentenceParser) :
    def __init__(self, wordsthreshold=300000):
        super().__init__()
        self.wordsthreshold = wordsthreshold
        print("Init Trainer")
        self.lock = Lock()

    def setwordlimit(self, wordsthreshold):
        self.wordsthreshold = wordsthreshold

    def buildVocab(self) :
        if len(self.wordmap.words) < 3:
            return

        for word in self.wordmap.words.values():
            self.scoreword(word)
        
        snglist, ylist, clist, ambilist = classifyHeads(self.wordmap.words.values())

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
        self.lock.acquire()
        try:
            if len(self.wordmap.words) > self.wordsthreshold:
                self.buildVocab()
            return None
        finally:
            self.lock.release()
        

    



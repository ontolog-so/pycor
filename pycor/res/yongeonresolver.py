import pycor.resolver as resolver
import pycor.utils as utils
import pycor.speechmodel as sm

__all__ = ["YongeonResolver"]

yongeonTags = set(['EFN'])
cheeonTags = set(['JKP','JKP-pp','JKS'])
cheeonPos = set(['C','NN','NP'])

class YongeonResolver(resolver.Resolver):
    def __init__(self, phraseMap={}):
        self.phraseMap = phraseMap
        self.tagsetIndex = {}

    def resolveDocument(self, sentence_array, context):
        for sentence in sentence_array:
            self.resolveWordGroup(sentence, context, self.phraseMap,self.tagsetIndex)
        
    def resolveWordGroup(self,sentence, context, phraseMap, tagsetIndex):
        for index, pair in enumerate(sentence.pairs):
            if issubclass(type(pair), sm.WordGroup):
                self.resolveWordGroup(pair, context, phraseMap,tagsetIndex)
            else:
                if len(yongeonTags & set(pair.tags))>0 and len(cheeonTags & set(pair.tags))==0:

                    if len(cheeonPos & pair.head.pos) > 0:
                        continue

                    pmap = phraseMap.get(pair.head)
                    if pmap is None:
                        pmap = {}
                        phraseMap[pair.head] = pmap

                    phrase = []
                    texts = []
                    tags = []
                    # phrase.append(word)
                    texts.append(pair.text)

                    if index > 1:
                        prev = sentence.words[index-1]
                        if type(prev) is sm.Word:
                            phrase.append(prev)
                            texts.append(prev.text)
                            if prev.bestpair:
                                tags.append('+'.join(prev.bestpair.tags))

                            if index > 2:
                                prev = sentence.words[index-2]
                                if type(prev) is sm.Word:
                                    phrase.append(prev)
                                    texts.append(prev.text)
                                    if prev.bestpair:
                                        tags.append('+'.join(prev.bestpair.tags))
                                

                    text = ' '.join(reversed(texts))
                    tagtext = ':'.join(reversed(tags))

                    if pmap.get(text) is None:
                        wl = list(reversed(phrase))
                        pmap[text] = wl
                    
                    headset = tagsetIndex.get(tagtext)

                    if tagsetIndex.get(tagtext) is None:
                        headset = set()
                        tagsetIndex[tagtext] = headset
                    headset.add(pair.head)

    def clssifyYongEon(self):
        for head, pmap in self.phraseMap.items():
            # if len(cheeonPos & head.pos) > 0:
            #     print("head is C", head)
            #     # continue

            tags = []

            for text, m in pmap.items():
                for w in m:
                    if w.bestpair:
                        tags.append('+'.join(w.bestpair.tags))
                    else :
                        tags.append(w.text)
            
            total = len(tags)

            if total>0:
                jko = float(tags.count('JKO') / total)
                jkbFm = float(tags.count('JKB-FM') / total)
                jkbBy = float(tags.count('JKB-TT|AS|BY') / total)
                jkbTo = float(tags.count('JKB-TO') / total)
                jks = float(tags.count('JKS') / total)
                jxso = float(tags.count('JX-SO') / total)

                if jko > 0.3:
                    head.addpos('T')
                    
                if jkbFm > 0.3:
                    head.addpos('D1')
                    
                if jkbBy > 0.3 or jkbTo > 0.3:
                    head.addpos('D2')
                    
                if jks > 0.3 or jxso > 0.3:
                    head.addpos('I')


    #########################
    ##  
    #########################
    def writemap(self, path):
        import csv
        import time
        starttime = time.time()
        with open(path, 'w', encoding='utf-8') as csvfile :
            writer = csv.writer(csvfile)
            self.phraseMap

            for head, pmap in self.phraseMap.items():
                for text, m in pmap.items():
                    row = []
                    row.append(head.text)
                    row.append(head.pos)
                    row.append(text)
                    tags = []
                    for w in m:
                        if w.bestpair:
                            tags.append('+'.join(w.bestpair.tags))
                        else :
                            tags.append(w.text)
                    
                    row.append(':'.join(tags))
                    writer.writerow(row)

            csvfile.close()
        print("Save ", path,  "  소요시간:" , round(time.time() - starttime, 3))

    #########################
    ##  
    #########################
    def writeindex(self, path):
        import csv
        import time
        starttime = time.time()
        with open(path, 'w', encoding='utf-8') as csvfile :
            writer = csv.writer(csvfile)
            self.phraseMap

            for tags, hset in self.tagsetIndex.items():
                for head in hset:
                    row = []
                    row.append(tags)
                    row.append(head.text)
                    writer.writerow(row)

            csvfile.close()
        print("Save ", path,  "  소요시간:" , round(time.time() - starttime, 3))

                    
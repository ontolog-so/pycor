import pycor.resolver as resolver
import pycor.utils as utils
import pycor.speechmodel as sm

__all__ = ["YongeonResolver"]

yongeonTags = set(['EFN'])
cheeonTags = set(['JKP','JKP-pp','JKS'])
cheeonPos = set(['C','NN','NP'])

class Phrase:
    def __init__(self):
        self.words = []
        self.pairs = []

    def add(self, word, pair):
        self.words.append(word)
        self.pairs.append(pair)

    def reverse(self):
        self.words.reverse()
        self.pairs.reverse()

    def clear(self):
        del self.words[:]
        del self.pairs[:]


class YongeonResolver(resolver.Resolver):
    def __init__(self, phraseMap={}):
        self.phraseMap = phraseMap
        self.tagsetIndex = {}

    def resolveDocument(self, sentence_array, context):
        phrase = Phrase() 
        for sentence in sentence_array:
            self.resolveWordGroup(sentence, context, self.phraseMap, self.tagsetIndex, phrase)
            # print(phrase.pairs)
            # phrase.clear()
        
    def resolveWordGroup(self,sentence, context, phraseMap, tagsetIndex, phrase):
        for index, pair in enumerate(sentence.pairs):
            if issubclass(type(pair), sm.WordGroup):
                phrase2 = Phrase() 
                self.resolveWordGroup(pair, context, phraseMap,tagsetIndex,phrase2)
            else:
                if len(yongeonTags & set(pair.tags))>0 and len(cheeonTags & set(pair.tags))==0:

                    if len(cheeonPos & pair.head.pos) > 0:
                        continue

                    pmap = phraseMap.get(pair.head)
                    if pmap is None:
                        pmap = {}
                        phraseMap[pair.head] = pmap

                    # phrase.add(sentence.words[index], pair)

                    pairs = []
                    texts = []
                    tags = []
                    # phrase.append(word)
                    texts.append(pair.text)

                    if index > 1:
                        prev = sentence.words[index-1]
                        if type(prev) is sm.Word:
                            pairs.append(prev)
                            texts.append(prev.text)
                            if prev.bestpair:
                                tags.append('+'.join(prev.bestpair.tags))
                                # phrase.add(prev, prev.bestpair)
                            # else:
                            #     phrase.add(prev, prev.particles[0])

                            if index > 2:
                                prev = sentence.words[index-2]
                                if type(prev) is sm.Word:
                                    pairs.append(prev)
                                    texts.append(prev.text)
                                    if prev.bestpair:
                                        tags.append('+'.join(prev.bestpair.tags))
                                        # phrase.add(prev, prev.bestpair)
                                    # else:
                                    #     phrase.add(prev, prev.particles[0])
                                

                    text = ' '.join(reversed(texts))
                    tagtext = ':'.join(reversed(tags))

                    if pmap.get(text) is None:
                        wl = list(reversed(pairs))
                        pmap[text] = wl
                    
                    headset = tagsetIndex.get(tagtext)

                    if tagsetIndex.get(tagtext) is None:
                        headset = set()
                        tagsetIndex[tagtext] = headset
                    headset.add(pair.head)
        # phrase.reverse()

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

                    
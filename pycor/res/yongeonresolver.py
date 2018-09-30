import pycor.resolver as resolver
import pycor.utils as utils
import pycor.speechmodel as sm

__all__ = ["YongeonResolver"]

yongeonTags = set(['EFN'])

class YongeonResolver(resolver.Resolver):
    def __init__(self, phraseMap={}):
        self.phraseMap = phraseMap
        self.tagsetIndex = {}

    def resolveDocument(self, sentence_array, context):
        for sentence in sentence_array:
            self.resolveSentence(sentence, context, self.phraseMap,self.tagsetIndex)
        
    def resolveSentence(self,sentence, context, phraseMap, tagsetIndex):
        for index, word in enumerate(sentence.words):
            if type(word) is sm.Sentence :
                self.resolveSentence(word, context, phraseMap,tagsetIndex)
            else:
                if word.bestpair and len(yongeonTags & set(word.bestpair.tags))>0 :
                    pmap = phraseMap.get(word.bestpair.head)
                    if pmap is None:
                        pmap = {}
                        phraseMap[word.bestpair.head] = pmap

                    phrase = []
                    texts = []
                    phrase.append(word)
                    texts.append(word.text)

                    if index > 1:
                        prev = sentence.words[index-1]
                        if type(prev) is sm.Word:
                            phrase.append(prev)
                            texts.append(prev.text)
                            if index > 2:
                                prev = sentence.words[index-2]
                                if type(prev) is sm.Word:
                                    phrase.append(prev)
                                    texts.append(prev.text)

                    text = ' '.join(reversed(texts))
                    tagtext = ':'.join(reversed(texts[:len(texts)-1]))

                    if pmap.get(text) is None:
                        wl = list(reversed(phrase))
                        pmap[text] = wl
                    
                    headset = tagsetIndex.get(tagtext)

                    if tagsetIndex.get(tagtext) is None:
                        headset = set()
                        tagsetIndex[tagtext] = headset
                    headset.add(word.bestpair.head)


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
                    row.append(text)
                    for w in m:
                        if w.bestpair:
                            row.append('+'.join(w.bestpair.tags))
                        else :
                            row.append(w.text)
                    
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

                    
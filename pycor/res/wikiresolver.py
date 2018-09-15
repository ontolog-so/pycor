import pycor.speechmodel as sm

__all__ = ["WikiResolver"]

class WikiResolver:
    def __init__(self, wordmap=None):
        print("Init WikiResolver")
        self.wordmap = wordmap
        
    
    def setwordmap(self, wordmap):
        self.wordmap = wordmap
    
    def resolveSentence(self,sentence):
        if len(sentence.words) == 1:
            keyword = self.checkEntry(sentence.words[0])
        return sentence

    def resolveKeywords(self, words_array):
        keywords = []
        for words in words_array:
            if len(words) == 1:
                keyword = self.checkEntry(words[0])
                keywords.append(keyword)
        return keywords

    def checkEntry(self, word):
        if word.bestpair:
            tail = word.bestpair.tail
            if tail != sm._VOID_Tail:
                word = self.wordmap.registerKeyword(word.text, "C")
            else:
                word.bestpair.head.addpos("C")
        else:
            word = self.wordmap.registerKeyword(word.text, "C")
        
        return word
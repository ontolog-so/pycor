import pycor.speechmodel as sm
import pycor.resolver as resolver

__all__ = ["WikiResolver"]

class WikiResolver(resolver.Resolver):
    
    def resolveDocument(self, sentence_array, context):
        for sentence in sentence_array:
            self.resolveSentence(sentence, context)
    
    def resolveSentence(self,sentence, context):
        if len(sentence.words) == 1:
            keyword = self.checkEntry(sentence.words[0], context)
        return sentence

    def resolveKeywords(self, words_array, context):
        keywords = []
        for words in words_array:
            if len(words) == 1:
                keyword = self.checkEntry(words[0], context)
                keywords.append(keyword)
        return keywords

    def checkEntry(self, word, context):
        if type(word) is sm.Word:
            if word.bestpair:
                tail = word.bestpair.tail
                if tail != sm._VOID_Tail:
                    word = context.registerKeyword(word.text, "C")
                else:
                    word.bestpair.head.addpos("C")
            else:
                word = context.registerKeyword(word.text, "C")
        
        return word
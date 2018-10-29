import pycor.resolver as resolver
import pycor.utils as utils
import pycor.speechmodel as sm

__all__ = ["SentenceResolver"]


class SentenceResolver(resolver.Resolver):
    def __init__(self, filepath):
        self.file = open(filepath,"w", encoding="UTF-8")

    def writeline(self, arr):
        line = ""
        for w in arr:
            line += w + " "
        self.file.write(line)
        self.file.write("\n")
        self.file.flush()

    def resolveDocument(self, sentence_array, context):
        for sentence in sentence_array:
            array = []
            self.resolveWordGroup(sentence, context,array)

            if len(array)>3:
                self.writeline(array)

    def resolveWordGroup(self,wordgroup, context, array):
        for index, pair in enumerate(wordgroup.pairs):
            if issubclass(type(pair), sm.Quote):
                if pair.first:
                    array.append(pair.first)
                self.resolveWordGroup(pair, context,array)
                if pair.last:
                    array.append(pair.last)
            elif issubclass(type(pair), sm.Sentence):
                array.append("\"")
                self.resolveWordGroup(pair, context,array)
                array.append("\"")
            else:
                if len(pair.head.text)>0:
                    array.append(pair.head.text)
                if len(pair.tail.text)>0:
                    array.append(pair.tail.text)
            
            
            

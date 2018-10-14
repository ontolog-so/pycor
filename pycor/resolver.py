import pycor.speechmodel as sm


def def_resolvesentence(sentence, context):
    __resolvesentence(sentence, context)

def __resolvesentence(sentence, context):
    for index, word in enumerate(sentence.words):
        if issubclass(type(word), sm.WordGroup):
            sentence.addpair(__resolvesentence(word, context))
        elif word.bestpair :
            sentence.addpair(word.bestpair)
        else :
            print("NO Bestpair", word.text)
    return sentence


"""
Document Resolver
"""
class Resolver:

    def resolveDocument(self, sentence_array, context ):
        pass



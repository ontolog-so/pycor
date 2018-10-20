import pycor.speechmodel as sm


"""
Document Resolver
"""
class Resolver:
    def resolveDocument(self, sentence_array, context ):
        pass


# class Clause:
#     def __init__(self):
#         self.words = []
#         self.pairs = []

#     def add(self, word, pair):
#         self.words.append(word)
#         self.pairs.append(pair)

#     def reverse(self):
#         self.words.reverse()
#         self.pairs.reverse()

#     def clear(self):
#         del self.words[:]
#         del self.pairs[:]


# def def_resolvesentence(sentence, documentContext):
#     __resolveWordGroup(sentence, documentContext)

# def __resolveWordGroup(wordgroup, documentContext):
#     for index, word in enumerate(wordgroup.words):
#         if issubclass(type(word), sm.WordGroup):
#             wordgroup.addpair(__resolveWordGroup(word, documentContext))
#         elif word.bestpair :
#             wordgroup.addpair(word.bestpair)
#         else :
#             raise Exception("NO Best pair "+ word.text)
#     return wordgroup



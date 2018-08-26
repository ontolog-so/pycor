
from pycor import trainer, parser, docresolver, utils, korutils
from pycor.std import *

__all__ = ["setmodel", "loadmodel", "savemodel","train", "buildvocab", "readfile", "readtext",
            "trim","trimfile","keywords","keywordsFromText", "setwordlimit", 
            "printSentences", "abstract", "abstractKeywords","totexts"]

ESC_TAGS = set(['MM','DN','NNB', 'PT','QS','QE','QM','VOID','EC','CL','SC'])

#############################
# Singletons
#############################
_trainer = trainer.Trainer()
_wordmap = _trainer.wordmap

_resolver = docresolver.DocResolver()
_resolver.setwordmap(_wordmap)

def setwordlimit(limit):
    _trainer.setwordlimit(limit)

def setmodel(wordmap):
    _wordmap = wordmap
    _trainer.setmodel(wordmap)

def loadmodel(model_dir):
    _trainer.loadmodel(model_dir)

def savemodel(model_dir):
    _trainer.savemodel(model_dir)

def train(data_dir, pattern="*.txt", limit=0):
    """ Load training data """
    stopwatch = utils.StopWatch()
    filelist = utils.listfiles(data_dir,pattern)
    index = 0
    if limit > 0:
        filelist = filelist[:limit]

    print("Loading Training Data - size:", len(filelist) )

    for file in filelist:
        _trainer.train(file)
        index += 1
        if index % 100 == 0:
            print(index,end=">")
            if index % 1000 == 0:
                print()
    print("Trained ", index, "files : ellapsed time", stopwatch.millisecstr(), "ms.")

def buildvocab():
    _trainer.buildVocab()

def readfile(filepath):
    """
    return sentence_array, wordObjs_array(2d)
    """
    return _trainer.loadfile(filepath)


def readtext(text):
    """
    return sentence_array, wordObjs_array(2d)
    """
    return _trainer.readtext(text)


def trim(text):
    """
    return words_array (2d), tags_array(2d)
    """
    _, words_array = _trainer.readtext(text)
    return __trim(words_array)

def trimfile(filepath):
    """
    return words_array (2d), tags_array(2d)
    """
    _, words_array = _trainer.loadfile(filepath)
    return __trim(words_array)

def __trim(words_array):
    rtns_array = []
    tags_array = []
    for sentence in words_array:
        words = []
        tags = []
        for word in sentence:
            if word.bestpair:
                if len(ESC_TAGS & word.bestpair.head.pos) == 0:
                    words.append(word.bestpair.head.text)
                    tags.append(word.bestpair.tags)
            else:
                words.append(word.text)
                tags.append([])
        if len(words)>0:
            rtns_array.append(words)
            tags_array.append(tags)
    return rtns_array,tags_array


def keywords(words_array, rate=0.05):
    """
    return dictionary {keywod:count,...}
    """
    return _resolver.extractKeywords(words_array,rate)


def keywordsFromText(text, rate=0.05):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    return dictionary {keywod:count,...}
    """
    _,words_array = readtext(text)
    return _resolver.extractKeywords(words_array,rate)


def abstractKeywords(words_array, rate=0.05, count=3):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    param count : 문장 개수  , 기본값 3
    return keywords, sentences
    """
    keywords = _resolver.extractKeywords(words_array, rate)
    if len(keywords) < 1:
        rate /= 2
        keywords = _resolver.extractKeywords(words_array, rate)

    sentences = _resolver.abstractDocument(keywords, words_array, count)
    return keywords, sentences


def abstract(text, rate=0.05, count=3):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    param count : 문장 개수 , 기본값 3
    return keywords, sentences
    """
    _,words_array = readtext(text)
    return abstractKeywords(words_array,rate, count)

def printSentences(sentences):
    docresolver.printSentences(sentences)

# line단위 텍스트로 변환
# return string array
def totexts(sentences):
    lines = []
    for sentence in sentences:
        aline =[]
        for word in sentence:
            aline.append(word.text)
        lines.append(' '.join(aline))
    return lines

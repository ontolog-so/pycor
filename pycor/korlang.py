
from pycor import trainer, parser, keywordutils, utils, korutils, resolver, dictionary
import pycor.speechmodel as sm
from pycor.std import *

__all__ = ["getmodel", "setmodel", "loadmodel", "loaddic", "savemodel","addresolver", "removeresolver",
            "train", "trainfiles", "buildvocab", "readfile", "readtext", "resolveword", "setscorefunction",
            "trim","trimfile","__trim", "keywords","keywordsFromText", "setwordlimit", 
            "printSentences", "abstract", "abstractKeywords","totexts", "registerKeyword",
            "debugword"]

ESC_TAGS = set(['MM','DN','NNB', 'PT','QS','QE','BS','BE' ,'QM','VOID','EC','CL','SC'])

#############################
# Singletons
#############################
_trainer = trainer.Trainer()
_wordmap = _trainer.wordmap

_keywordutils = keywordutils.KeywordUtils()
_keywordutils.setwordmap(_wordmap)


def setwordlimit(limit):
    _trainer.setwordlimit(limit)

def getmodel():
    return _wordmap
    
def setmodel(wordmap):
    _wordmap = wordmap
    _trainer.setmodel(wordmap)

def loadmodel(model_dir):
    _trainer.loadmodel(model_dir)

def loaddic(dic_path):
    _trainer.loaddic(dic_path)
    
def savemodel(model_dir):
    _trainer.savemodel(model_dir)

def addresolver(resolver):
    _trainer.addresolver(resolver)

def removeresolver(resolver):
    _trainer.removeresolver(resolver)

def registerKeyword(keyword, pos):
    _wordmap.registerKeyword(keyword, pos)

def resolveword(text, debug=False):
    return _trainer.resolveword(text,debug)

def setscorefunction(fn):
    _trainer.scorefunction = fn

def train(data_dir, pattern="*.txt", limit=0, debugPath=None):
    """ Load training data """
    filelist = utils.listfiles(data_dir,pattern)
    if limit > 0:
        filelist = filelist[:limit]

    trainfiles(filelist, debugPath)
    

def trainfiles(filelist, debugPath=None):
    print("Loading Training Data - size:", len(filelist) )
    stopwatch = utils.StopWatch()

    debugWriter = None
    debugfile = None

    if debugPath:
        import csv
        debugfile = open(debugPath+"/debug_words.csv", 'w', encoding='utf-8')
        debugWriter = csv.writer(debugfile)
        
    index = 0
    for file in filelist:
        _trainer.train(file,debugWriter)
        index += 1
        if index % 100 == 0:
            print(index,end=">")
            if index % 1000 == 0:
                print()
    
    buildvocab(debugWriter)

    if debugfile:
        debugfile.close()

    print("Trained ", index, "files : ellapsed time", stopwatch.millisecstr(), "ms.")

# return snglist, ylist, clist, ambilist
def buildvocab(debugWriter=None):
    return _trainer.buildVocab(debugWriter)

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
    sentences = _trainer.readtext(text)
    return __trim(sentences)

def trimfile(filepath):
    """
    return words_array (2d), tags_array(2d)
    """
    sentences = _trainer.loadfile(filepath)
    return __trim(sentences)

def __trim(sentences):
    rtns_array = []
    tags_array = []
    for sentence in sentences:
        __trimwordgroup(sentence, rtns_array, tags_array)
    return rtns_array,tags_array

def __trimwordgroup(wordgroup, rtns_array, tags_array):
        words = []
        tags = []
        for pair in wordgroup.pairs:
            if issubclass(type(pair), sm.WordGroup):
                __trimwordgroup(pair, rtns_array, tags_array)
            elif len(ESC_TAGS & pair.head.pos) == 0:
                words.append(pair.head.text)
                tags.append(pair.tags)
                
        if len(words)>0:
            rtns_array.append(words)
            tags_array.append(tags)

def keywords(sentence_array, rate=0.05):
    """
    return dictionary {keywod:count,...}
    """
    return _keywordutils.extractKeywords(sentence_array,rate)


def keywordsFromText(text, rate=0.05):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    return dictionary {keywod:count,...}
    """
    _,words_array = readtext(text)
    return _keywordutils.extractKeywords(words_array,rate)


def abstractKeywords(sentences, rate=0.05, count=3):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    param count : 문장 개수  , 기본값 3
    return keywords, sentences
    """
    keywords = _keywordutils.extractKeywords(sentences, rate)
    if len(keywords) < 1:
        rate /= 2
        keywords = _keywordutils.extractKeywords(sentences, rate)

    sentences = _keywordutils.abstractDocument(keywords, sentences, count)
    return keywords, sentences


def abstract(text, rate=0.05, count=3):
    """
    param rate : 0~1 사이의 float, 기본값 0.05
    param count : 문장 개수 , 기본값 3
    return keywords, sentences
    """
    sentences = readtext(text)
    return abstractKeywords(sentences,rate, count)

def printSentences(sentences):
    keywordutils.printSentences(sentences)

# 여러 Sentence객체들을 문장 단위 텍스트 배열로 변환
# return string array
def totexts(sentences):
    lines = []
    for sentence in sentences:
        line = keywordutils._toTextWordGroup(sentence)
        lines.append(line)
    return lines

def debugword(word):
    for pair in word.particles:
        print (pair)
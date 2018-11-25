import pycor.bisect.tree as tr
import pycor.bisect.chain as ch
import pycor.parser as parser
import pycor.morpheme as mor
import pycor.speechmodel as sm
import time

def readfiles(filelist, limit=0):
    startTime = time.time()

    tree = tr.Tree()
    tree.loadfiles(filelist, limit)

    print("Files loaded. Ellapsed time:", (time.time() - startTime))

    # newRoot = tree.rebuildtree()

    wordmap = buildWordMap(tree.root)
    print("WordMap built. Ellapsed time:", (time.time() - startTime))

    print("Words Count:", len(wordmap.words.values()))
    
    print("Heads Count:", len(wordmap.heads))
    print("Tails Count:", len(wordmap.tails))
    
    classfyHeads(wordmap.heads.values(), wordmap)

    endTime = time.time()
    print("Ellapsed time:", (endTime - startTime))
    return wordmap


def buildWordMap(treeRoot) :
    wordmap = sm.WordMap()
    ambiguosMap = {}
    wordTokens = parser.WordTokens('')
    
    for node in treeRoot.children.values():
        buildword(node,"",wordmap,wordTokens, ambiguosMap)
    

    return wordmap

def buildword(node, prevtext, wordmap, wordTokens,ambiguosMap):
    text = prevtext + node.ch

    if node.endCount>0:
        wordObj = wordmap.getword(text)
        if wordObj is None:
            wordObj = sm.Word(text)
            wordmap.addword(wordObj)
            wordTokens.set(text)
            auxs = mor.getAuxs(wordTokens.prev())
            if auxs:
                maxPair = None
                maxPairs = []
                curidx = wordTokens.curidx
                for aux in auxs:
                    headtails = aux.procede(wordTokens, None, wordObj, None, None, None)
                    if headtails:
                        for pair in headtails:
                            head = gethead(pair.head, wordmap)
                            tail = gettail(pair.tail, wordmap)
                            pair = score(pair, wordObj, head, tail, node)
                            tail.addtags(pair.tags)

                            if maxPair is None:
                                maxPair = pair
                            elif pair.score > maxPair.score:
                                maxPair = pair
                                del maxPairs[:]
                            elif pair.score == maxPair.score:
                                if pair.tail != maxPair.tail:
                                    maxPairs.append(maxPair)
                                    # print(pair.head , pair.tail, " -- ", maxPair.head, maxPair.tail)
                                    maxPair = pair
                                
                    wordTokens.setPos(curidx)

                if maxPair:
                    if len(maxPairs) == 0:
                        wordObj.addPair(maxPair)
                        addHeadPair(wordObj, maxPair.head, maxPair.tail, maxPair, node)
                        if maxPair.tail:
                            maxPair.tail.score += 1
                    else:
                        pairs = []
                        ambiguosMap[wordObj] = pairs
                        addHeadPair(wordObj, maxPair.head, maxPair.tail, maxPair, node)
                        pairs.append(maxPair)
                        for p in maxPairs:
                            addHeadPair(wordObj, p.head, p.tail, p, node)
                            pairs.append(p)
                        
    elif node.count()>3 :
        head = gethead(text, wordmap)

    for child in node.children.values():
        buildword(child,text,wordmap, wordTokens, ambiguosMap)

def classfyHeads(heads,wordmap):
    tags = set()
    for head in heads:
        for tailtext, pair in head.pairs.items():
            tail = wordmap.tails.get(tailtext)
            tags.update(tail.tags)

        ycount = 0
        ccount = 0
        for t in tags:
            if t.startswith('E'):
                ycount += 1
            elif t.startswith('J'):
                ccount += 1
        
        if ycount > ccount:
            head.addpos("Y")
        if ccount > (ycount + ccount)/2:
            head.addpos("C")
        tags.clear()


def addHeadPair(wordObj, head, tail, pair, node):
    head.score = pair.score
    pairInfo = head.addpair(tail.text, pair.score, pair.pos, pair.tags )
    pairInfo[3] = node.countDesc()

def score(pair, word, head, tail, node):
    pair.head = head
    pair.tail = tail
    score = 0.0

    if head:
        score += head.occurrence() + head.score

    if tail:
        score += len(tail.text)

    if pair.ambi:
        if head.score<1:
            score -= 1.5 + head.score
        # if node.parent:
        #     if node.parent.count() > node.endCount:
        #         score -= 1.5

    pair.score = score

    return pair

def gethead(text, wordmap):
    head = wordmap.heads.get(text)
    
    if head is None:
        if len(text) == 0:
            head = sm._VOID_Head
        else:
            head = sm.Head(text)
        wordmap.heads[text] = head
    return head

def gettail(text, wordmap):
    tail = wordmap.tails.get(text)
    
    if tail is None:
        if text is None or len(text) == 0:
            tail = sm._VOID_Tail
        else :
            tail = sm.Tail(text)
        wordmap.tails[text] = tail
    return tail
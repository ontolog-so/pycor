import pycor.bisect.tree as tr
import pycor.bisect.chain as ch
import pycor.parser as parser
import pycor.morpheme as mor
import pycor.speechmodel as sm

def readfiles(data_dir, pattern="*.txt", limit=0):
    tree = tr.Tree()
    tree.loadfiles(data_dir, pattern, limit)

    chains = ch.Chains()
    chains.buildchains(tree.root)

    print("Build chains:", len(chains.segments.values()) )

    wordmap, wordlist = buildWordMap(chains)

    print("Build wordmap. Heads:", len(wordmap.heads) )

    bagOfHeads = set()

    wordTokens = parser.WordTokens('')

    for word in wordlist:
        extractWord(word, wordTokens, chains, wordmap, bagOfHeads)

    print("Extract Heads:", len(wordmap.heads) )

    # for head in bagOfHeads:
    #     print(head, head.tails)

    return wordmap

def extractWord(word, wordTokens, chains, wordmap, bagOfHeads):
    wordTokens.set(word)
    auxs = mor.getAuxs(wordTokens.prev())
    if auxs:
        wordObj = wordmap.getword(word)
        curidx = wordTokens.curidx
        for aux in auxs:
            headtails = aux.procede(wordTokens, None, wordObj, None, None, None)
            if headtails:
                maxPair = None
                for ht in headtails:
                    t = ht.tail
                    segment = chains.segments.get(ht.head)
                    head = wordmap.heads.get(ht.head)
                    tail = wordmap.tails.get(t)
                    pair = score(word, head, tail, segment)

                    if maxPair is None:
                        maxPair = pair
                    elif pair.score > maxPair.score:
                        maxPair = pair
                    elif pair.score == maxPair.score:
                        maxPair = pair

                if maxPair.head:
                    maxPair.head.score = maxPair.score
                    bagOfHeads.add(maxPair.head)
                    maxPair.head.addpair(tail.text, maxPair.score, maxPair.pos, maxPair.tags )
                    # if segment:
                    #     bagOfWords.add(segment.text)
                    #     for prev in segment.prevs.keys():
                    #         bagOfWords.add(prev)


            wordTokens.setPos(curidx)

def score(word, head, tail, segment):
    pair = sm.Pair(word,head,tail)
    score = 0.0
    if head:
        score += head.occurrence()
    if tail:
        score += len(tail.text)
    
    pair.score = score

    return pair

def buildWordMap(chains) :
    wordmap = sm.WordMap()
    wordTokens = parser.WordTokens('')
    wordlist = []
    for segment in chains.segments.values():
        text = segment.text
        if segment.prevCount() == 0 and segment.endCount>0:
            # print(text,segment.prevCount(),segment.nextCount(),segment.endCount)
            auxs = mor.getAuxs(text[len(text)-1])
            if auxs:
                wordlist.append(text)
                wordObj = wordmap.getword(text)
                wordTokens.set(text)
                wordTokens.prev()
                curidx = wordTokens.curidx
                for aux in auxs:
                    headtails = aux.procede(wordTokens, None, wordObj, None, None, None)
                    if headtails:
                        for ht in headtails:
                            t = ht.tail
                            head = wordmap.heads.get(ht.head)
                            tail = wordmap.tails.get(t)
                            if tail is None:
                                if t is None or len(t) == 0:
                                    tail = sm._VOID_Tail
                                else :
                                    tail = sm.Tail(t)
                                wordmap.tails[t] = tail
                            if head :
                                tail.appendhead(head)
                                head.appendtail(tail)
                            # print(">", ht.head, tail)
                            # if chains.hasSegment(ht.head):
                            #     seg = chains.getSegment(ht.head)
                            #     if seg.nextCount() > 0:
                                    # print("> segment :", seg.text, seg.nextCount(), tail) 
                    wordTokens.setPos(curidx)
            elif segment.nextCount() > 0:
                wordmap.getOrNewHead(text)
        elif segment.nextCount() > 0 and segment.endCount > 0 and len(segment.text) > 1 and segment.prevCount()<segment.nextCount():
            wordmap.getOrNewHead(text)
    
    # for head in wordmap.heads.values():
    #     print(head, head.tails)

    # for tail in wordmap.tails.values():
    #     print(tail)

    # for word in wordlist:
    #     print(word)

    return wordmap, wordlist

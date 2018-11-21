import os
import math
import pycor.speechmodel as sm

cheeonPos = {"C","NP","NN","NNB","ISM"}
yoneonPos = {"Y","V"}

def default_scorepair(pair, word, context, prevWords, nextWords):
    score = pair.score

    hs = pair.head.score/pair.head.occurrence()

    penalty = 0.0

    # if pair.ambi:
    #     hs += pair.head.score * 0.7
    #     if pair.head.score<1:
    #         penalty += 1 -pair.head.score
    # else :
    #     hs += pair.head.occurrence() * 0.1
    
    if pair.ambi:
        # hs += pair.head.score * 0.7
        if pair.head.score<1:
            penalty += 1.5 -pair.head.score
    # else :
    #     hs += pair.head.occurrence() * 0.1

    ts = 0.0
    
    if pair.tail :
        # ts = (pair.tail.occurrence() *0.009) - (len(pair.tail.text) * 0.09)
        ts = len(pair.tail.text) 

    
    if len(cheeonPos & pair.head.pos)>0:
        if not('JKP' in pair.tags):
            for t in pair.tags:
                if t.startswith("E"):
                    penalty += 1

    elif len(yoneonPos & pair.head.pos)>0: 
        for t in pair.tags:
            if t.startswith("J"):
                penalty += 1
            elif t == "EPT-pr":
                penalty -= 1

    try:
        # pair.score = 1/(1 + math.e**(-hs-score + ts + penalty) )
        pair.score = hs + score + ts - penalty
    except Exception as e:
        print(e)
        print(hs, score, ts)
    

    return pair

# def old_scorepair(pair, word, context):
#     # score = pair.score * 2
#     score = pair.score

#     hs = 0
#     ts = 0

#     hs = pair.head.occurrence() + pair.head.score
#     hs = hs * 1.3
    
#     if pair.tail:
#         ts = pair.tail.occurrence()
    
#     # pair.score = hs - (ts*0.09) + (score * 10)
#     pair.score = hs - (ts*0.09) + score

#     return pair

def default_choosepair(candidates, context, prevWord, nextWord):
    length = len(candidates)
    if length == 1:
        return candidates[0]
    else:
        maxPair = None
        for pair in candidates:
            if maxPair is None or pair.head.score > maxPair.head.score:
                maxPair = pair

        return maxPair

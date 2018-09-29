import os
import math
import pycor.speechmodel as sm

def default_scorepair(pair, word, context):
    score = pair.score
    hs = pair.head.occurrence()
    ts = 0.0
    
    if pair.tail:
        ts = pair.tail.occurrence() *0.009

    try:
        pair.score = 1/(1 + math.e**(-hs-score + ts) )
    except Exception as e:
        print(e)
        print(hs, score, ts)
    

    return pair

def old_scorepair(pair, word, context):
    # score = pair.score * 2
    score = pair.score

    hs = 0
    ts = 0

    hs = pair.head.occurrence() + pair.head.score
    hs = hs * 1.3
    
    if pair.tail:
        ts = pair.tail.occurrence()
    
    # pair.score = hs - (ts*0.09) + (score * 10)
    pair.score = hs - (ts*0.09) + score

    return pair

def alt_scorepair(pair, word, context):
    score = pair.score
    hs = pair.head.occurrence()
    ts = 0.0
    
    if pair.tail:
        ts = pair.tail.occurrence() *0.009

    try:
        pair.score = 1/(1 + math.e**(-hs-score + ts) )
    except Exception as e:
        print(e)
        print(hs, score, ts)
    

    return pair

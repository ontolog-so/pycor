import sys
import pycor.speechmodel as sm

def loadmodel(modeldir):
    wordmap = sm.WordMap()
    wordmap.load(modeldir)
    return wordmap

def compareHeads(oldHeads, newHeads):
    old = oldHeads.copy()
    compArr = []

    for key, val in newHeads.items():
        if val.score:
            if key in old:
                oldh = old[key]
                del old[key]
                union = oldh.pos.union(val.pos)
                if len(union) != len(oldh.pos):
                    compArr.append( ['o',oldh] )
                    compArr.append( ['n',val] )
            else:
                compArr.append( ['+',val] )

    for oval in old.values():
        compArr.append( ['-',oval] )
    
    return compArr


def saveCompHeads(path, compArr):
    import csv
    with open(path, 'w', encoding='utf-8') as csvfile :
        writer = csv.writer(csvfile)
        list = sorted(compArr, key=lambda kv: kv[1].text)
        for kv in list:
            writer.writerow([kv[0], kv[1].text, '+'.join(kv[1].pos)]) 
        csvfile.close()
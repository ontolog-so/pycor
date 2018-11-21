from pycor import utils

class Segment:
    def __init__(self, text):
        self.text = text
        self.prevs = {}
        self.nexts = {}
        self.endCount = 0

    def addPrev(self, prevSeg):
        joint = self.prevs.get(prevSeg.text)
        if joint is None:
            joint = Joint(prevSeg, self)
            self.prevs[prevSeg.text] = joint
        joint.addcount()
        return self

    def addNext(self, nextSeg):
        joint = self.nexts.get(nextSeg.text)
        if joint is None:
            joint = Joint(self, nextSeg)
            self.nexts[nextSeg.text] = joint
        joint.addcount()
        return self

    def nextCount(self):
        return len(self.nexts)

    def prevCount(self):
        return len(self.prevs)

    def countEnd(self):
        self.endCount += 1

class Joint:
    def __init__(self, prevSeg, nextSeg):
        self.prevSeg = prevSeg
        self.nextSeg = nextSeg
        self.count = 0

    def addcount(self):
        self.count += 1

class Chains:
    def __init__(self):
        self.segments = {}
        
    def hasSegment(self, text):
        segment = self.segments.get(text)
        return segment != None

    def getSegment(self, text):
        segment = self.segments.get(text)
        if segment is None:
            segment = Segment(text)
            self.segments[text] = segment
        return segment

    def buildchains(self, root):
        for node in root.children.values():
            self.bisect(node,None,'')  

    def bisect(self, node, prevSeg, buf):
        text = buf + node.ch
        if node.endCount>0 or node.count()>1:
            segment = self.getSegment(text)
            prevText = None
            if prevSeg:
                prevSeg.addNext(segment)
                segment.addPrev(prevSeg)
                prevText = prevSeg.text + segment.text
            else:
                prevText = segment.text
            prevSeg = self.getSegment(prevText)
            text = ''
            if node.endCount>0 :
                prevSeg.countEnd()
                if prevSeg != segment:
                    segment.countEnd()
        
        for child in node.children.values():
            self.bisect(child,prevSeg,text)
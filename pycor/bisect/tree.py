from pycor import utils

# CH_WORD_END = chr(31)

class Quote:
    def __init__(self,start,end):
        self.start = start
        self.end = end

quoteclues = {
    '「':Quote('「','」'),
    '‘':Quote('‘','’'),
    '“':Quote('“','”'),
    '"':Quote('"','"'),
    '(':Quote('(',')'),
    '[':Quote('[',']'),
    '{':Quote('{','}'),
    '\'':Quote('\'','\''),
    '\"':Quote('\"','\"'),
    '《':Quote('《','》'),
    '〈':Quote('〈','〉'),
    '⟪':Quote('⟪','⟫'),
    '｢':Quote('｢','｣'),
    '＜':Quote('＜','＞'),
    '［':Quote('［','］'),
    '（':Quote('（','）'),
    '『':Quote('『','』'),
    '<':Quote('<','>')   
    }

def isdigit(text, index):
    if index<0 or len(text) -1 < index:
        return False
    return text[index].isdigit() 

class Node:
    def __init__(self, parent, ch):
        self.ch = ch
        self.parent = parent
        self.children = {}
        self.endCount = 0
    
    def getChild(self, ch):
        cn = self.children.get(ch)
        if cn is None:
            cn = Node(self, ch)
            self.children[ch] = cn
        return cn
    
    # 자기 아래 후손들의 전체 개수 
    def countDesc(self):
        cnt = len(self.children)
        for chn in self.children.values():
            cnt += chn.countDesc()
        return cnt

    # 자기 아래 후손들의 전체 개수 
    def count(self):
        return len(self.children)

    def prnt(self, indent):
        print(indent, self.ch, self.count())
        indent += "."

        for chn in self.children.values():
            chn.prnt(indent)

    def countEnd(self):
        self.endCount += 1

class Tree:
    def __init__(self):
        self.root = Node(None,'')
        
    def digestword(self, word):
        length = len(word)
        index = 0
        node = self.root
        while index<length:
            ch = word[index]
            node = node.getChild(ch)
            index += 1
        node.countEnd()

    def readrow(self,text):
        length = len(text)
        index = 0
        word = ''
        while index < length:
            ch = text[index]
            if ch in quoteclues:
                end = text.find(quoteclues[ch].end, index+1)
                word = word.strip()
                if(len(word) > 0):
                    self.digestword(word)
                word = ''
                if end > index:
                    arr = self.readrow(text[index+1:end])
                    index = end +1
                else:
                    index +=1 
            else:
                if ch in ['.','?','!',':',';','\n']:
                    if ch == '.' and (isdigit(text, index-1) or isdigit(text, index+1)) :
                        word += ch
                        index += 1
                        continue

                    word = word.strip()

                    if(len(word) > 0):
                        self.digestword(word)
                        word = ''
                elif ch in [' ','　',' ',' ',',','\n','\r']:
                    word = word.strip()
                    if(len(word) > 0):
                        self.digestword(word)
                        word = ''
                elif ch in ['-','_']:
                    word += ch
                elif ch.isalpha() or ch.isdigit():
                    word += ch
                index += 1

        word = word.strip()
        if len(word) > 0:
            self.digestword(word)


    def loadfile(self, path):
        # print("reading", path)
        print(".", end="")
        with open(path, 'r', encoding='utf-8') as file :
            lines = file.readlines()
            for row in lines:
                self.readrow(row)  
            file.close()


    def loadFromDir(self,data_dir, pattern="*.txt", limit=0):
        """ Load training data """
        filelist = utils.listfiles(data_dir,pattern)
        if limit > 0:
            filelist = filelist[:limit]

        for index, file in enumerate(filelist):
            self.loadfile(file)
            if index % 100 == 0:
                print(" > ", index)
        print('')

    def loadfiles(self,filelist, limit=0):
        if limit > 0:
            filelist = filelist[:limit]

        for index, file in enumerate(filelist):
            self.loadfile(file)
            if index % 100 == 0:
                print(" > ", index)
        print('')
        
    def whitenodes(self, path):
        import csv
        with open(path, 'w', encoding='utf-8') as file :
            writer = csv.writer(file)
            for node in self.root.children.values():
                self.writenode(node,'',writer)  

    def writenode(self, node, buf, writer):
        buf += node.ch
        if node.endCount>0:
            writer.writerow([buf, node.count(), node.endCount])
        elif node.count()>1:
            writer.writerow([buf, node.count()])
        
        for child in node.children.values():
            self.writenode(child,buf,writer)


    def rebuildtree(self):
        newRoot = Node('')

        for node in self.root.children.values():
            self.rebuildnode(node,'',newRoot)

        return newRoot

    def rebuildnode(self, node, buf, parent):
        buf += node.ch
        
        if node.count()>1 or node.endCount>0:
            parent = parent.getChild(buf)
            parent.endCount = node.endCount
            buf = ''
        
        for child in node.children.values():
            self.rebuildnode(child,buf,parent)

    def treetoarray(self, root):
        rootarray = []

        for node in root.children.values():
            arrs = self.nodetoarrays(node,None)
            rootarray.extend(arrs)
        return rootarray

    def nodetoarrays(self, node, prev):
        rtnArr = []

        arr = []
        if prev:
            arr.extend(prev)

        if node.count()>1 or node.endCount>0:
            arr.append(node.ch)
            rtnArr.append(arr)

        for child in node.children.values():
            arrs = self.nodetoarrays(child,arr)
            rtnArr.extend(arrs)
        
        return rtnArr
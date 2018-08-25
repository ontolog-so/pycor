import time
import math
import csv

class StopWatch():
    def __init__(self):
        self.start()
        
    def __repr__(self) :
        return self.timestr()
    
    def start(self):
        self.starttime = time.time()
        self.ellpased = 0.0
        return self
    
    def stop(self):
        self.ellpased = time.time() - self.starttime
        self.starttime = 0
    
    def time(self):
        if self.ellpased > 0:
            return self.ellpased
        else :
            return time.time() - self.starttime  
    
    # HH:mm:ss
    def hms(self):
        return self.__format( self.time() )
    
    
    # millisec
    def millisec(self):
        return int(self.time() * 1000)
    
    
    # millisecstr 천 단위 ,로 구분된 밀리세컨드 
    def millisecstr(self):
        return "{:,}".format(self.millisec())
    
    # 
    def sec(self):
        return math.floor(self.time())
    
    # 
    def secmilli(self):
        t = self.time()
        s = math.floor(t)
        m = int(round( (t - s) * 1000))
        return '{:d}s.{:03d}ms.'.format(int(s), m)
    
    def __format(self, t):
        t = int(t)
        return ('{:02d}:{:02d}:{:02d}'.format(t // 3600, (t % 3600 // 60), t % 60))
    
    
def comma(number):
    return "{:,}".format(number)


def writecsv(path, datalist, handler):
    stopwatch = StopWatch().start()
    
    with open(path, 'w', encoding='utf-8') as csvfile :
        writer = csv.writer(csvfile)
        for data in datalist:
            handler(writer, data)
        csvfile.close()
    print("Write ", path,  "  소요시간:" , stopwatch.secmilli() , "(", stopwatch.millisecstr(), "ms.)" )


def listfiles(path, pattern=None, cascade=True):
    import fnmatch
    import os

    result_arr = []
    filenames = os.listdir(path)
    for filename in filenames:
        full_filename = os.path.join(path, filename)
        if os.path.isdir(full_filename):
            if cascade:
                lst = listfiles(full_filename, pattern, cascade)
                result_arr.extend(lst)
        else:
            if pattern:
                if fnmatch.fnmatch(filename, pattern):
                    result_arr.append(full_filename)
            else:
                result_arr.append(full_filename)
    return result_arr

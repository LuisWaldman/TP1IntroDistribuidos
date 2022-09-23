from os import SEEK_END
from os import SEEK_SET

class Fragmentador:
    file = ''
    mss = 1

    def __init__(self, filename, mss):
        self.file = open(filename, 'rb')
        self.mss = mss

    def getBytesFromFile(self, package):
        if package > 0:
            self.file.seek(self.mss*(package-1), SEEK_SET)
            return self.file.read(self.mss)
        return 0

    def close(self):
        self.file.close()

    def getTotalSize(self):
        self.file.seek(0, SEEK_END)
        return self.file.tell()
from os import SEEK_END

class Desfragmentador:
    file = ''
    mss = 1

    def __init__(self, filename, size, mss):
        self.file = open(filename, "wb")
        self.mss = mss

    def setBytesToFile(self, bytes, package):
        self.file.seek(0)
        self.file.seek(self.mss * (package - 1))
        return self.file.write(bytes)

    def close(self):
        self.file.close()
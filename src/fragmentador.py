from os import SEEK_END
from os import SEEK_SET


class Fragmentador:
    file = ''
    mss = 1

    def __init__(self, file, mss):
        self.file = file
        self.mss = mss

    def get_bytes_from_file(self, package):
        if package > 0:
            self.file.seek(self.mss*(package-1), SEEK_SET)
            return self.file.read(self.mss)
        return 0

    def close(self):
        self.file.close()

    def get_total_size(self):
        self.file.seek(0, SEEK_END)
        return self.file.tell()

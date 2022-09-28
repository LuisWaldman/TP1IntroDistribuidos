class Desfragmentador:
    file = ''
    mss = 1

    def __init__(self, file, mss):
        self.file = file
        self.mss = mss

    def set_bytes_to_file(self, data, package):
        self.file.seek(0)
        self.file.seek(self.mss * (package - 1))
        return self.file.write(data)

    def close(self):
        self.file.close()

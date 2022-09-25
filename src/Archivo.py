import os


class Archivo:
    TAMANO_MAXIMO = 5000000  # 5MB

    def __init__(self, ruta):
        self.ruta = ruta

    def excede_tamano_limite(self):
        estadisticas = os.stat(self.ruta)
        return estadisticas.st_size > self.TAMANO_MAXIMO

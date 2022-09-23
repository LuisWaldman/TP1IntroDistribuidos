
from src.salida import EnumSalida


class Parametros:
    mostrar_ayuda = False
    enum_salida = EnumSalida.INFORMACION
    ip = "localhost"
    port = 10666
    path = ""
    filename = ""

    def __init__(self, parametros):
        cargando = ""

        for par in parametros:
            if par == "-h":
                self.mostrar_ayuda = True
                cargando = ""
            elif par == "-v":
                self.enum_salida = EnumSalida.VERBORRAGICA
                cargando = ""
            elif par == "-q":
                self.enum_salida = EnumSalida.NINGUNA
                cargando = ""
            elif par in ('-H', '-p', '-s', '-n'):
                cargando = par
            else:
                if cargando == "-H":
                    self.ip = par
                elif cargando == "-p":
                    self.port = par
                elif cargando == "-s":
                    self.path = par
                elif cargando == "-n":
                    self.filename = par

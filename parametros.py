
from salida import *
class Parametros:
    mostrarayuda = False
    enumSalida = EnumSalida.Informacion
    IP = "localhost"
    port = 10666
    path = ""
    filename = ""


    def __init__(self, parametros):
        cargando = ""

        for par in parametros:
            if par == "-h":
                self.mostrarayuda = True
                cargando = ""
            elif par == "-v":
                self.enumSalida = EnumSalida.Verborragica
                cargando = ""
            elif par == "-q":
                self.enumSalida = EnumSalida.Ninguna
                cargando = ""
            elif par == "-H" or par == "-p" or par == "-s" or par == "-d" or par == "-n":
                cargando = par
            else:
                if cargando == "-H":
                    self.IP = par
                elif cargando == "-p":
                    self.port = par
                elif cargando == "-s" or cargando == "-s":
                    self.path = par
                elif cargando == "-n":
                    self.filename = par

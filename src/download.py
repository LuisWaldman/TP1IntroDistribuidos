import sys
from src.salida import *
from src.parametros import *


param = Parametros(sys.argv)
if param.mostrar_ayuda:
    print("usage : download [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [ - d FILEPATH ] [ - n FILENAME ]")
    print("")
    print("< command description >")
    print("")
    print("optional arguments :")
    print("-h , -- help show this help message and exit")
    print("-v , -- verbose increase output verbosity")
    print("-q , -- quiet decrease output verbosity")
    print("-H , -- host server IP address")
    print("-p , -- port server port")
    print("-d , -- dst destination file path")
    print("-n , -- name file name")
    exit(0)

salida = Salida(param.enum_salida)
salida.info("Muestra informacion")
salida.verborragica("Muestra verborragica")

print("IP:", param.ip)
print("port:", param.port)
print("path:", param.path)
print("filename:", param.filename)


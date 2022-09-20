import sys
from salida import Salida
from parametros import Parametros


param = Parametros(sys.argv)
if param.mostrarayuda:
    print("usage : upload [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [ - s FILEPATH ] [ - n FILENAME ]")
    print("")
    print("< command description >")
    print("")
    print("optional arguments :")
    print("")
    print("    -h , -- help show this help message and exit")
    print("    -v , -- verbose increase output verbosity")
    print("    -q , -- quiet decrease output verbosity")
    print("    -H , -- host server IP address")
    print("    -p , -- port server port")
    print("    -s , -- src source file path")
    print("    -n , -- name file name")
    exit(0)

salida = Salida(param.enumSalida)
salida.Info("Muestra informacion")
salida.Verborragica("Muestra verborragica")

print("IP:", param.IP)
print("port:", param.port)
print("path:", param.path)
print("filename:", param.filename)

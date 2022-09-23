import sys
import yaml
from src.salida import Salida
from src.parametros import Parametros

with open('config.yaml', 'r', encoding='utf-8') as yaml_file:
    configs = yaml.safe_load(yaml_file)

param = Parametros(sys.argv)
if param.mostrar_ayuda:
    print(
        "usage : upload [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ]"
        "[ - s FILEPATH ] [ - n FILENAME ]"
    )
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
    sys.exit()

salida = Salida(param.enum_salida)
salida.info("Muestra informacion")
salida.verborragica("Muestra verborragica")

print("IP:", param.ip)
print("port:", param.port)
print("path:", param.path)
print("filename:", param.filename)

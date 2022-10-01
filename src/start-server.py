import sys
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from src.conexion.Servidor import Servidor

param = Parametros(sys.argv)
if param.mostrar_ayuda:
    print("usage : start - server [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ] [ - s DIRPATH ]")
    print("< command description >")
    print("optional arguments :")
    print("-h , -- help show this help message and exit")
    print("-v , -- verbose increase output verbosity")
    print("-q , -- quiet decrease output verbosity")
    print("-H , -- host service IP address")
    print("-p , -- port service port")
    print("-s , -- storage storage dir path")
    exit(0)
elif param.error:
    print(
        "usage : upload [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ]"
        "[ - s FILEPATH ] [ - n FILENAME ]"
    )
    exit(0)

salida = Salida(param.enum_salida)

salida.verborragica("IP:" + str(param.ip))
salida.verborragica("port:" + str(param.port))
salida.verborragica("path:" + str(param.path))
salida.verborragica("filename:" + str(param.filename))

servidor = Servidor(param.ip, param.port)
salida.info('Servidor iniciado')
servidor.escuchar()

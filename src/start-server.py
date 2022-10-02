import sys
import signal
import logging

from src.utils.parametros import Parametros
from src.conexion.Servidor import Servidor
from src.utils.signal import sigint_exit
from src.utils.log import set_up_log

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
    print("usage : start - server [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ] [ - s DIRPATH ]")
    exit(0)

signal.signal(signal.SIGINT, sigint_exit)
set_up_log(param.enum_salida)

logging.debug("IP:" + str(param.ip))
logging.debug("port:" + str(param.port))
logging.debug("path:" + str(param.path))
logging.debug("filename:" + str(param.filename))

servidor = Servidor(param.ip, param.port, param.path)
logging.info('Servidor iniciado')
servidor.escuchar()

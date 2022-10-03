import sys
import signal
import logging
from socket import socket, AF_INET, SOCK_DGRAM

from src.conexion import Conexion
from src.conexion.Receptor import Receptor
from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje
from src.utils.signal import sigint_exit
from src.utils.log import set_up_log

exit_code = 0

param = Parametros(sys.argv)
if param.filename == "":
    print('ERROR: Debe especificar un archivo')
    param.error = True

if param.mostrar_ayuda:
    print("usage : download [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ] [ - d FILEPATH ] [ - n FILENAME ]")
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

elif param.error:
    print("usage : download [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ] [ - d FILEPATH ] [ - n FILENAME ]")
    exit(0)

set_up_log(param.enum_salida)

logging.debug("IP:" + str(param.ip))
logging.debug("port:" + str(param.port))
logging.debug("path:" + str(param.path))
logging.debug("filename:" + str(param.filename))

signal.signal(signal.SIGINT, sigint_exit)

clientSocket = socket(AF_INET, SOCK_DGRAM)

if Conexion.establecer_conexion(clientSocket,
                                (param.ip, param.port),
                                param.filename,
                                TipoMensaje.DOWNLOAD):
    logging.debug("Recibiendo archivo...")
    receptor = Receptor(clientSocket, param.path + param.filename)
    direccion = receptor.recibir_archivo()
    receptor.esperar_cierre_conexion(direccion)

clientSocket.close()
logging.info("Comunicación terminada.")
exit(exit_code)

import sys
from socket import socket, AF_INET, SOCK_DGRAM
import signal
import logging

from src.conexion import Conexion
from src.conexion.Emisor import Emisor
from src.utils.Archivo import Archivo
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
    exit(0)
elif param.error:
    print(
        "usage : upload [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ]"
        "[ - s FILEPATH ] [ - n FILENAME ]"
    )
    exit(0)

set_up_log(param.enum_salida)

logging.debug("IP:" + str(param.ip))
logging.debug("port:" + str(param.port))
logging.debug("path:" + str(param.path))
logging.debug("filename:" + str(param.filename))

signal.signal(param.path, sigint_exit)

archivo = Archivo(param.path + param.filename)
if not archivo.existe():
    logging.info("El archivo que se intenta subir no existe")
    exit(5)

clientSocket = socket(AF_INET, SOCK_DGRAM)

(conexion_establecida, serverAddress) = Conexion.establecer_conexion(clientSocket, (param.ip, param.port), param.filename, TipoMensaje.UPLOAD)
if conexion_establecida:
    logging.debug("Enviando archivo...")
    emisor = Emisor(clientSocket, param.path + param.filename, serverAddress, param.protocoloN)
    emisor.enviar_archivo()

clientSocket.close()
logging.info("Comunicación terminada")
exit(exit_code)

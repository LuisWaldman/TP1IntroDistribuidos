import sys
import signal
import logging
from socket import socket, AF_INET, SOCK_DGRAM

from src.conexion.Receptor import Receptor
from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.signal import sigint_exit
from src.utils.log import set_up_log

MAX_PAYLOAD = 64000
TIMEOUT_SEGUNDOS = 2
INTENTOS_CONEXION = 5
exit_code = 0

param = Parametros(sys.argv)
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

logging.info("Iniciando comunicación")
tipo = TipoMensaje.HOLA + TipoMensaje.DOWNLOAD
primer_mensaje = Mensaje(tipo, 1, 1, param.filename)
primer_paquete = Traductor.MensajeAPaquete(primer_mensaje)

for i in range(0, INTENTOS_CONEXION):
    try:
        clientSocket.sendto(primer_paquete, (param.ip, param.port))
        logging.debug("Esperando paquete HELLO...")
        clientSocket.settimeout(TIMEOUT_SEGUNDOS)

        paquete_recibido, serverAddress = clientSocket.recvfrom(2048)
        logging.debug("Paquete HELLO recibido")
        mensaje_recibido = Traductor.PaqueteAMensaje(paquete_recibido, True)
        break

    except TimeoutError as e:
        if i < INTENTOS_CONEXION-1:
            logging.debug("Timeout: reenvio de paquete HELLO...")
        else:
            logging.info("No se pudo establecer la conexion")
            clientSocket.close()
            exit(5)

if mensaje_recibido.tipo_mensaje == TipoMensaje.HOLA:
    logging.debug("Recibiendo archivo...")
    clientSocket.settimeout(None)
    receptor = Receptor(clientSocket, param.path + param.filename)
    direccion = receptor.recibir_archivo()
    receptor.esperar_cierre_conexion(direccion)
elif mensaje_recibido.tipo_mensaje == TipoMensaje.ERROR:
    logging.info("Error: " + mensaje_recibido.payload)
    exit_code = 4
else:
    logging.info(
        f"Error: tipo de mensaje {TipoMensaje(mensaje_recibido.tipo_mensaje).name} inesperado."
    )
    exit_code = 5

clientSocket.close()
logging.info("Comunicación terminada.")
exit(exit_code)

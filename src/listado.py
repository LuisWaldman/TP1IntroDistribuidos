import sys
import signal
import logging
from socket import socket, AF_INET, SOCK_DGRAM

from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.signal import sigint_exit
from src.utils.log import set_up_log

MAX_PAYLOAD = 64000
TIMEOUT_SEGUNDOS = 2
INTENTOS_CONEXION = 1
exit_code = 0

param = Parametros(sys.argv)
if param.mostrar_ayuda:
    print("usage : listado [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ]")
    print("")
    print("< command description >")
    print("")
    print("optional arguments :")
    print("-h , -- help show this help message and exit")
    print("-v , -- verbose increase output verbosity")
    print("-q , -- quiet decrease output verbosity")
    print("-H , -- host server IP address")
    print("-p , -- port server port")
    exit(0)

elif param.error:
    print("usage : listado [ - h ] [ - v | -q ] [ - H ADDR ] "
          "[ - p PORT ]")
    exit(0)

set_up_log(param.enum_salida)

logging.debug("IP:" + str(param.ip))
logging.debug("port:" + str(param.port))

signal.signal(signal.SIGINT, sigint_exit)

clientSocket = socket(AF_INET, SOCK_DGRAM)

logging.info("Iniciando comunicación")
tipo = TipoMensaje.OBTENERLISTADO
primer_mensaje = Mensaje(tipo, 1, 1, param.filename)
primer_paquete = Traductor.MensajeAPaquete(primer_mensaje)

for i in range(0, INTENTOS_CONEXION):
    try:
        clientSocket.sendto(primer_paquete, (param.ip, param.port))
        logging.debug("Espera el paquete con el listado...")
        clientSocket.settimeout(TIMEOUT_SEGUNDOS)

        paquete_recibido, serverAddress = clientSocket.recvfrom(2048)
        logging.debug("Paquete respuesta recibido")
        mensaje_recibido = Traductor.paquete_a_mensaje(paquete_recibido, True)
        print(mensaje_recibido.payload)
        break

    except TimeoutError:
        if i < INTENTOS_CONEXION-1:
            logging.debug("Timeout: reenvio de paquete de listado...")
        else:
            logging.info("No se pudo establecer la conexion")
            clientSocket.close()
            exit(5)

clientSocket.close()
logging.info("Comunicación terminada.")
exit(exit_code)

import sys
import signal
from socket import socket, AF_INET, SOCK_DGRAM

from src.conexion.Receptor import Receptor
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.signal import sigint_exit

MAX_PAYLOAD = 64000

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


Salida.enumsalida = param.enum_salida

Salida.verborragica("IP:" + str(param.ip))
Salida.verborragica("port:" + str(param.port))
Salida.verborragica("path:" + str(param.path))
Salida.verborragica("filename:" + str(param.filename))

signal.signal(signal.SIGINT, sigint_exit)

clientSocket = socket(AF_INET, SOCK_DGRAM)

Salida.info("Iniciando comunicacion")
tipo = TipoMensaje.HOLA + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
primermensaje = Mensaje(tipo, 1, 1, param.filename)
primerpaquete = Traductor.MensajeAPaquete(primermensaje)
clientSocket.sendto(primerpaquete, (param.ip, param.port))

Salida.verborragica("esperando respuesta hello ...")
paqueterecibido, serverAddress = clientSocket.recvfrom(2048)
Salida.verborragica("paquete recibido")
mensajerecibido = Traductor.PaqueteAMensaje(paqueterecibido, False)

if(mensajerecibido.tipo_mensaje == TipoMensaje.HOLA):
    Salida.verborragica("recepción de respuesta hello")
    receptor = Receptor(clientSocket, param.path + param.filename)
    receptor.recibir_archivo()

clientSocket.close()
Salida.info("comunicacion terminada")

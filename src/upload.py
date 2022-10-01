import sys
import math
from socket import socket, AF_INET, SOCK_DGRAM

from src.utils.salida import Salida
from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.fragmentador import Fragmentador

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
    exit(0)
elif param.error:
    print(
        "usage : upload [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ]"
        "[ - s FILEPATH ] [ - n FILENAME ]"
    )
    exit(0)

Salida.enumsalida = param.enum_salida

Salida.verborragica("IP:" + str(param.ip))
Salida.verborragica("port:" + str(param.port))
Salida.verborragica("path:" + str(param.path))
Salida.verborragica("filename:" + str(param.filename))


Salida.verborragica("Inicio Parametros")
mss = 100


clientSocket = socket(AF_INET, SOCK_DGRAM)

Salida.info("Iniciando comunicacion STOP & WAIT")
tipo_mensaje = TipoMensaje.HOLA + TipoMensaje.UPLOAD + TipoMensaje.STOPANDWAIT
primermensaje = Mensaje(tipo_mensaje, 1, 1, "")
primerpaquete = Traductor.MensajeAPaquete(primermensaje)
clientSocket.sendto(primerpaquete, (param.ip, param.port))
terminoarhivo = False

with open(param.path + param.filename, "rb") as file_origen:
    frag = Fragmentador(file_origen, param.mss)
    parte = 1
    total_size = frag.get_total_size()
    num_packages = math.ceil(total_size / param.mss)
    while parte <= num_packages:
        bytesleidos = frag.get_bytes_from_file(parte)
        mensajeparte = Mensaje(TipoMensaje.PARTE, num_packages, parte, bytesleidos)
        paqueteparte = Traductor.MensajeAPaquete(mensajeparte)
        clientSocket.sendto(paqueteparte, clientAddress)
        message, clientAddress = clientSocket.recvfrom(2048)
        mensaje = Traductor.PaqueteAMensaje(message)
        if mensajeparte.tipo_mensaje == TipoMensaje.ACK:
            parte = parte + 1

clientSocket.close()
Salida.info("comunicacion terminada")

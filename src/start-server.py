import sys
import math
from socket import socket, AF_INET, SOCK_DGRAM
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from src.utils.Traductor import Traductor
from src.utils.fragmentador import Fragmentador
from src.mensajes.mensaje import TipoMensaje, Mensaje


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

salida.info("Inicio Servidor")
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((param.ip, param.port))
salida.info("El servidor está listo para recibir")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    mensaje = Traductor.PaqueteAMensaje(message)
    if mensaje.tipo_mensaje == TipoMensaje.HOLA:
        salida.verborragica("Llega mensaje HOLA")
        if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD and mensaje.tipo_protocolo == TipoMensaje.STOPANDWAIT:
            salida.verborragica("Un DOWNLOAD EN STOP & WAIT")
            salida.info("Descargando archivo: " + mensaje.payload)
            with open(param.path + mensaje.payload, "rb") as file_origen:
                frag = Fragmentador(file_origen, param.mss)
                parte = 1
                total_size = frag.get_total_size()
                num_packages = math.ceil(total_size / param.mss)
                while parte <= num_packages:
                    bytesleidos = frag.get_bytes_from_file(parte)
                    mensajeparte = Mensaje(TipoMensaje.PARTE, num_packages, parte, bytesleidos)
                    paqueteparte = Traductor.MensajeAPaquete(mensajeparte)
                    serverSocket.sendto(paqueteparte, clientAddress)
                    message, clientAddress = serverSocket.recvfrom(2048)
                    mensaje = Traductor.PaqueteAMensaje(message)
                    if mensajeparte.tipo_mensaje == TipoMensaje.ACK:
                        parte = parte + 1


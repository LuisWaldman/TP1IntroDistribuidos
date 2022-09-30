import sys
import math
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from socket import socket, AF_INET, SOCK_DGRAM
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


salida = Salida(param.enum_salida)

salida.verborragica("IP:" + str(param.ip))
salida.verborragica("port:" + str(param.port))
salida.verborragica("path:" + str(param.path))
salida.verborragica("filename:" + str(param.filename))


salida.verborragica("Inicio Parametros")
mss = 100


clientSocket = socket(AF_INET, SOCK_DGRAM)

salida.info("Iniciando comunicacion STOP & WAIT")
tipo_mensaje = TipoMensaje.HOLA + TipoMensaje.UPLOAD + TipoMensaje.STOPANDWAIT
primermensaje = Mensaje(tipo_mensaje, 1, 1, "")
primerpaquete = Traductor.MensajeAPaquete(primermensaje)
clientSocket.sendto(primerpaquete, (param.ip, param.port))
terminoarhivo = False

frag = Fragmentador(param.filename, mss)
parte = 0

total_size = frag.get_total_size()
num_packages = math.ceil(total_size / mss)
while parte < num_packages:

    salida.verborragica("esperando paquete ...")
    paqueterecibido, serverAddress = clientSocket.recvfrom(2048)
    salida.verborragica("paquete recibido")
    mensajerecibido = Traductor.PaqueteAMensaje(paqueterecibido)

    aux = frag.get_bytes_from_file(parte)
    salida.verborragica("Bytes Escritos" + aux)

    mensajeAck = Mensaje(TipoMensaje.ACK, 1, 1, mensajerecibido.parte)
    paqueteack = Traductor.MensajeAPaquete(mensajeAck)
    salida.verborragica("Envia ACK parte" + mensajerecibido.parte)
    clientSocket.sendto(paqueteack, (param.ip, param.port))
    if mensajerecibido.parte == mensajerecibido.total_partes:
        terminoarhivo = True

clientSocket.close()
salida.info("comunicacion terminada")

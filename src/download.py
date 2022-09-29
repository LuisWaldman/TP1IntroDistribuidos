import sys
from src.utils.salida import *
from src.utils.parametros import *
from socket import *
from src.mensajes.mensaje import *
from src.utils.Traductor import *

param = Parametros(sys.argv)
if param.mostrar_ayuda:
    print("usage : download [ - h ] [ - v | -q ] [ - H ADDR ] [ - p PORT ] [ - d FILEPATH ] [ - n FILENAME ]")
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


salida = Salida(param.enum_salida)

salida.verborragica("IP:" + str(param.ip))
salida.verborragica("port:" + str(param.port))
salida.verborragica("path:"+ str(param.path))
salida.verborragica("filename:" + str(param.filename))


clientSocket = socket(AF_INET, SOCK_DGRAM)

primermensaje = Mensaje_hola(EnumOperacion.DOWNLOAD, EnumProtocolo.STOPANDWAIT)
message = Traductor.MensajeAPaquete(primermensaje)
clientSocket.sendto(message, (param.ip, param.port))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
salida.info(modifiedMessage.decode())
clientSocket.close()

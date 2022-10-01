import sys
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from socket import socket, AF_INET, SOCK_DGRAM
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.desfragmentador import Desfragmentador


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


Salida.verborragica("Inicio Parametros")
mss = 100

clientSocket = socket(AF_INET, SOCK_DGRAM)

Salida.info("Iniciando comunicacion STOP & WAIT")
tipo = TipoMensaje.HOLA + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
primermensaje = Mensaje(tipo, 1, 1, param.filename)
primerpaquete = Traductor.MensajeAPaquete(primermensaje)
clientSocket.sendto(primerpaquete, (param.ip, param.port))
terminoarhivo = False

desfrag = Desfragmentador(param.filename, mss)
while not terminoarhivo:

    Salida.verborragica("esperando paquete ...")
    paqueterecibido, serverAddress = clientSocket.recvfrom(2048)
    Salida.verborragica("paquete recibido")
    mensajerecibido = Traductor.PaqueteAMensaje(paqueterecibido)

    aux = desfrag.set_bytes_to_file(mensajerecibido.payload,
                                    mensajerecibido.parte)
    Salida.verborragica("Bytes Escritos" + aux)

    mensajeAck = Mensaje(TipoMensaje.ACK, 1, 1, mensajerecibido.parte)
    paqueteack = Traductor.MensajeAPaquete(mensajeAck)
    Salida.verborragica("Envia ACK parte" + mensajerecibido.parte)
    clientSocket.sendto(paqueteack, (param.ip, param.port))
    if mensajerecibido.parte == mensajerecibido.total_partes:
        terminoarhivo = True

clientSocket.close()
Salida.info("comunicacion terminada")

import sys
import socket, AF_INET, SOCK_DGRAM
import signal

from src.conexion.Emisor import Emisor
from src.utils.salida import Salida
from src.utils.parametros import Parametros
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.signal import sigint_exit

exit_code = 0

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

signal.signal(signal.SIGINT, sigint_exit)

clientSocket = socket(AF_INET, SOCK_DGRAM)

Salida.info("Iniciando comunicacion")
tipo_mensaje = TipoMensaje.HOLA + TipoMensaje.UPLOAD + TipoMensaje.STOPANDWAIT
print(f'tipo_mensaje: {tipo_mensaje}')
primer_mensaje = Mensaje(tipo_mensaje, 1, 1, param.filename)
primer_paquete = Traductor.MensajeAPaquete(primer_mensaje)
clientSocket.sendto(primer_paquete, (param.ip, param.port))
termino_archivo = False

Salida.verborragica("Esperando paquete HELLO...")
paquete_recibido, serverAddress = clientSocket.recvfrom(2048)
Salida.verborragica("Paquete HELLO recibido")
mensaje_recibido = Traductor.PaqueteAMensaje(paquete_recibido, True)

if mensaje_recibido.tipo_mensaje == TipoMensaje.HOLA:
    Salida.verborragica("Enviando archivo...")
    emisor = Emisor(clientSocket, param.path + param.filename, serverAddress)
    emisor.enviar_archivo()
if mensaje_recibido.tipo == TipoMensaje.ERROR:
    Salida.info("Error: " + mensaje_recibido.payload)
    exit_code = 4
else:
    Salida.info(
        "Error: tipo de mensaje {} inesperado.".format(mensaje_recibido.tipo)
    )
    exit_code = 5
# todo cerrar conexion

clientSocket.close()
Salida.info("Comunicación terminada")
exit(exit_code)

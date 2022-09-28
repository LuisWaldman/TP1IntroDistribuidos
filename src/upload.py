import sys
from utils.salida import *
from utils.parametros import *
from socket import *

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
salida.verborragica("path:"+ str(param.path))
salida.verborragica("filename:" + str(param.filename))

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = "mensaje en minucula"
clientSocket.sendto(message.encode(), (param.ip, param.port))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
salida.info(modifiedMessage.decode())
clientSocket.close()

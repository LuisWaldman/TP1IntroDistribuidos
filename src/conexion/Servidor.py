from socket import socket, AF_INET, SOCK_DGRAM
import threading
from src.mensajes.mensaje import TipoMensaje
from src.utils.Traductor import Traductor
from src.utils.salida import Salida

class Servidor:
    BUFER_MAXIMO = 1024

    def __init__(self, ip, puerto):
        self.conexion = socket(AF_INET, SOCK_DGRAM)
        self.conexion.bind((ip, puerto))
        self.clientes = list()

    def escuchar(self):
        Salida.info("Escuchando ...")
        while True:
            mensaje, direccion = self.conexion.recvfrom(self.BUFER_MAXIMO)
            if self.nueva_conexion(mensaje, direccion):
                hilo = threading.Thread(target=self.atender_cliente,
                                        args=(mensaje.decode(), direccion))
                hilo.start()

    def nueva_conexion(self, mensaje, direccion):
        mensaje = Traductor.PaqueteAMensaje(mensaje)

        if int(str(mensaje.tipo)[0]) == TipoMensaje.HOLA:
            if direccion in self.clientes:
                return False

            self.clientes.append(direccion)
            print("Llego un mensaje para iniciar la comunicacion")
            return True
        # todo faltaria chequear que quiere y la existencia de archivo
        return False

    def atender_cliente(self, mensaje, direccion):
        print('funcionalidad del thread')

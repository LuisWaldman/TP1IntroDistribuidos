from socket import socket, AF_INET, SOCK_DGRAM
import threading
import pathlib
from src.mensajes.mensaje import TipoMensaje
from src.utils.Traductor import Traductor
from src.utils.Archivo import Archivo


class Servidor:
    BUFER_MAXIMO = 1024

    def __init__(self, ip, puerto):
        self.conexion = socket(AF_INET, SOCK_DGRAM)
        self.conexion.bind((ip, puerto))
        self.clientes = list()

    def escuchar(self):
        while True:
            mensaje, direccion = self.conexion.recvfrom(self.BUFER_MAXIMO)
            if self.nueva_conexion(mensaje, direccion):
                hilo = threading.Thread(target=self.atender_cliente,
                                        args=(mensaje.decode(), direccion))
                hilo.start()

    def nueva_conexion(self, mensaje, direccion):
        mensaje = Traductor.PaqueteAMensaje(mensaje)
        (tipo, operacion, protocolo) = self.obtener_tipo_mensaje(mensaje)

        if tipo == TipoMensaje.HOLA:
            if direccion in self.clientes:
                return False

            src_path = str(pathlib.Path(__file__).parent.parent.absolute())
            if operacion == TipoMensaje.DOWNLOAD:
                archivo = Archivo(src_path + '/server_files/' + mensaje.payload)
                if not archivo.existe():
                    return False
            else:
                archivo = Archivo(src_path + '/download_files/' + mensaje.payload)
                if archivo.existe():
                    return False

            self.clientes.append(direccion)
            return True

        return False

    def atender_cliente(self, mensaje, direccion):
        print('funcionalidad del thread') # todo

    def obtener_tipo_mensaje(self, mensaje):
        tipos_str = str(mensaje.tipo)
        return (int(tipos_str[0]), int(tipos_str[1])*10, int(tipos_str[2])*100)
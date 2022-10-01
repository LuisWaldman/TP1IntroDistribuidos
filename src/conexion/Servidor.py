from socket import socket, AF_INET, SOCK_DGRAM
import threading
import pathlib
from src.mensajes.mensaje import TipoMensaje
from src.utils.Traductor import Traductor
from src.utils.salida import Salida
from src.utils.Archivo import Archivo

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

            Salida.verborragica("Mensaje recibido. Abriendo hilo para el nuevo cliente")

            hilo = threading.Thread(target=self.atender_cliente,
                                    args=(mensaje.decode(), direccion))
            hilo.start()

    def nueva_conexion(self, mensaje, direccion):
        if mensaje.tipo_mensaje == TipoMensaje.HOLA:
            Salida.info("Mensaje recibido para iniciar conexión")
            if direccion in self.clientes:
                Salida.verborragica("Conexión existente. Desacarto mensaje")
                return False

            src_path = str(pathlib.Path(__file__).parent.parent.absolute())
            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                Salida.verborragica("Conexión de tipo DOWNLOAD")
                archivo = Archivo(src_path + '/server_files/' + mensaje.payload)
                if not archivo.existe():
                    Salida.verborragica("Archivo solicitado no existente")
                    return False
                Salida.verborragica("Archivo solicitado existente")
            else:
                Salida.verborragica("Conexión de tipo UPLOAD")
                archivo = Archivo(src_path + '/download_files/' + mensaje.payload)
                if archivo.existe():
                    Salida.verborragica("Archivo ofrecido existente")
                    return False
                Salida.verborragica("Archivo ofrecido inexistente")

            self.clientes.append(direccion)
            Salida.verborragica("Nuevo cliente agregado al servidor")
            return True

        return False

    def atender_cliente(self, mensaje, direccion):
        mensaje = Traductor.PaqueteAMensaje(mensaje)

        if self.nueva_conexion(mensaje, direccion):
            Salida.verborragica("Atendiendo")

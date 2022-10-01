from socket import socket, AF_INET, SOCK_DGRAM
import threading
# import pathlib
from src.mensajes.mensaje import TipoMensaje
from src.utils.Traductor import Traductor
from src.utils.salida import Salida
from src.utils.Archivo import Archivo

class Servidor:
    BUFER_MAXIMO = 1024

    def __init__(self, ip, puerto, dirpath):
        self.conexion = socket(AF_INET, SOCK_DGRAM)
        self.conexion.bind((ip, puerto))
        self.dirpath = dirpath
        self.clientes = list()
        self.lock = threading.Lock()

    def escuchar(self):
        Salida.info("Escuchando ...")
        while True:
            mensaje, direccion = self.conexion.recvfrom(self.BUFER_MAXIMO)

            Salida.verborragica("Mensaje recibido. Abriendo hilo para el nuevo cliente")

            hilo = threading.Thread(target=self.atender_cliente,
                                    args=(self.lock, mensaje.decode(), direccion))
            hilo.start()
            # todo ver lo del join

    def nueva_conexion(self, lock, mensaje, direccion):
        if mensaje.tipo_mensaje == TipoMensaje.HOLA:
            Salida.info("Mensaje recibido para iniciar conexión")

            lock.acquire()
            if direccion in self.clientes:
                Salida.verborragica("Conexión existente. Desacarto mensaje")
                return False

            #src_path = str(pathlib.Path(__file__).parent.parent.absolute())

            archivo = Archivo(self.dirpath)
            existe = archivo.existe()

            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                Salida.verborragica("Conexión de tipo DOWNLOAD")
                if not existe:
                    Salida.verborragica("Archivo solicitado inexistente")
                    return False
                Salida.verborragica("Archivo solicitado existente")

            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                Salida.verborragica("Conexión de tipo UPLOAD")
                if existe:
                    Salida.verborragica("Archivo ofrecido existente")
                    return False
                Salida.verborragica("Archivo ofrecido inexistente")

            self.clientes.append(direccion)
            lock.release()

            Salida.verborragica("Nuevo cliente agregado al servidor")
            return True

        return False

    def atender_cliente(self, lock, mensaje, direccion):
        mensaje = Traductor.PaqueteAMensaje(mensaje)

        if self.nueva_conexion(lock, mensaje, direccion):
            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                Salida.verborragica("Atendiendo: cliente=receptor servidor=emisor")
            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                Salida.verborragica("Atendiendo: cliente=emisor servidor=receptor")
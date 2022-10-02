from socket import socket, AF_INET, SOCK_DGRAM
import threading
from src.conexion.Receptor import Receptor
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
from src.utils.salida import Salida
from src.utils.Archivo import Archivo

from src.conexion.Emisor import Emisor


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

            Salida.info("Mensaje recibido. Abriendo hilo para el nuevo cliente")

            hilo = threading.Thread(target=self.atender_cliente,
                                    args=(mensaje, direccion))
            hilo.start()

    def nueva_conexion(self, mensaje, direccion):
        if mensaje.tipo_mensaje == TipoMensaje.HOLA:
            Salida.info("Mensaje recibido para iniciar conexión")

            self.lock.acquire()
            if direccion in self.clientes:
                Salida.info("Conexión existente. Desacarto mensaje")
                self.lock.release()
                return False

            archivo = Archivo(self.dirpath + mensaje.payload)
            existe = archivo.existe()

            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                Salida.info("Conexión de tipo DOWNLOAD")
                if not existe:
                    Salida.info("Archivo solicitado inexistente")
                    self.lock.release()
                    return False
                Salida.info("Archivo solicitado existente")

            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                Salida.info("Conexión de tipo UPLOAD")
                if existe:
                    Salida.info("Archivo ofrecido existente")
                    self.lock.release()
                    return False
                Salida.info("Archivo ofrecido inexistente")

            self.clientes.append(direccion)
            self.lock.release()

            Salida.info("Nuevo cliente agregado al servidor")
            return True

        return False

    def atender_cliente(self, mensaje, direccion):
        mensaje = Traductor.PaqueteAMensaje(mensaje, True)

        if self.nueva_conexion(mensaje, direccion):
            socket_atencion = socket(AF_INET, SOCK_DGRAM);
            self.responder(socket_atencion, direccion, mensaje.tipo_operacion)

            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                Salida.info("Atendiendo: cliente=receptor servidor=emisor")
                emisor = Emisor(socket_atencion, self.dirpath + mensaje.payload, direccion)
                emisor.enviar_archivo()
                # todo cerrar la conexion
            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                Salida.info("Atendiendo: cliente=emisor servidor=receptor")
                receptor = Receptor(socket_atencion, self.dirpath + mensaje.payload)
                receptor.recibir_archivo()
                # todo cerrar la conexion

    def responder(self, socket, direccion, tipo_operacion):
        Salida.info("Respondiendo mensaje hello")
        tipo = TipoMensaje.HOLA + tipo_operacion + TipoMensaje.STOPANDWAIT
        hello_response_msg = Mensaje(tipo, 1, 1, None)
        hello_response_pkg = Traductor.MensajeAPaquete(hello_response_msg)
        socket.sendto(hello_response_pkg, direccion)
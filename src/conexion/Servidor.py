import threading
import logging

from socket import socket, AF_INET, SOCK_DGRAM
from src.conexion.Receptor import Receptor
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor
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
        logging.info("Escuchando ...")
        while True:
            mensaje, direccion = self.conexion.recvfrom(self.BUFER_MAXIMO)

            logging.info("Mensaje recibido. Abriendo hilo para el nuevo cliente")

            hilo = threading.Thread(target=self.atender_cliente,
                                    args=(mensaje, direccion))
            hilo.start()

    def assert_message(self, mensaje, direccion):
        error = ""
        if mensaje.tipo_mensaje == TipoMensaje.HOLA:
            logging.info("Mensaje recibido para iniciar conexión")
            self.lock.acquire()
            if direccion in self.clientes:
                error = "Conexión existente. Desacarto mensaje"
                logging.info(error)
                self.lock.release()
                raise Exception(error)
            archivo = Archivo(self.dirpath + mensaje.payload)
            existe = archivo.existe()
            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                logging.info("Conexión de tipo DOWNLOAD")
                if not existe:
                    error = "El archivo solicitado no existe"
                    logging.info(error)
                    self.lock.release()
                    raise Exception(error)
                logging.info("Archivo solicitado existente")
            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                logging.info("Conexión de tipo UPLOAD")
                if existe:
                    error = "El archivo ofrecido existente"
                    logging.info(error)
                    self.lock.release()
                    raise Exception(error)
                logging.info("Archivo ofrecido inexistente")
            self.clientes.append(direccion)
            self.lock.release()
            logging.info("Nuevo cliente agregado al servidor")
        else:
            error = "Primer mensaje enviado por un cliente no fue HELLO"
            logging.info(error)
            raise Exception(error)

    def atender_cliente(self, paquete, direccion):
        mensaje = Traductor.PaqueteAMensaje(paquete, True)

        socket_atencion = socket(AF_INET, SOCK_DGRAM)
        try:
            self.assert_message(mensaje, direccion)
            self.responder(socket_atencion, direccion, mensaje.tipo_operacion)
            if mensaje.tipo_operacion == TipoMensaje.DOWNLOAD:
                logging.info("Atendiendo: cliente=receptor servidor=emisor")
                emisor = Emisor(socket_atencion, self.dirpath + mensaje.payload, direccion)
                emisor.enviar_archivo()
                logging.info("Conexion cerrada")
                # todo cerrar la conexion
            elif mensaje.tipo_operacion == TipoMensaje.UPLOAD:
                logging.info("Atendiendo: cliente=emisor servidor=receptor")
                receptor = Receptor(socket_atencion, self.dirpath + mensaje.payload)
                receptor.recibir_archivo()
                logging.info("Conexion cerrada")
                # todo cerrar la conexion
        except Exception as error:
            self.enviar_error(socket_atencion, str(error), direccion)

    def responder(self, socket, direccion, tipo_operacion):
        logging.info("Respondiendo mensaje hello")
        tipo = TipoMensaje.HOLA + tipo_operacion
        hello_response_msg = Mensaje(tipo, 1, 1, None)
        hello_response_pkg = Traductor.MensajeAPaquete(hello_response_msg)
        socket.sendto(hello_response_pkg, direccion)
    
    def enviar_error(self, socket, error, direccion):
        logging.info("Enviando mensaje de error")
        hello_response_msg = Mensaje(TipoMensaje.ERROR, 1, 1, error)
        hello_response_pkg = Traductor.MensajeAPaquete(hello_response_msg)
        socket.sendto(hello_response_pkg, direccion)

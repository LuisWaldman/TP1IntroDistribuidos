import logging

from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor


def hello_ack(socket, address):
    logging.debug('Enviando HELLO ACK...')
    tipo = TipoMensaje.HOLA_ACK + TipoMensaje.DOWNLOAD
    msg_hello_ack = Mensaje(tipo, 1, 1, None)
    pkg_hello_ack = Traductor.MensajeAPaquete(msg_hello_ack)
    socket.sendto(pkg_hello_ack, address)
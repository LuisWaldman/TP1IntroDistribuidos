import logging

from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor

INTENTOS_CONEXION = 5
TIMEOUT_SEGUNDOS = 2


def establecer_conexion(socket, address, filename, tipo_mensaje):
    logging.debug("Estableciendo conexión...")

    for i in range(0, INTENTOS_CONEXION):
        enviar_hello(socket, address, filename, tipo_mensaje)
        socket.settimeout(TIMEOUT_SEGUNDOS)
        try:
            pkg, serverAddres = socket.recvfrom(2048)
            logging.debug("Paquete recibido")
            msg = Traductor.paquete_a_mensaje(pkg, False)

            if msg.tipo_mensaje == TipoMensaje.ERROR:
                logging.info("Error " + msg.payload.decode())
                return (False, None)
            if msg.tipo_mensaje != TipoMensaje.HOLA:
                continue

            socket.settimeout(None)
            logging.debug("Paquete HELLO RESPONSE recibido")
            enviar_hello_ack(socket, serverAddres)
            break
        except TimeoutError:
            if i < INTENTOS_CONEXION - 1:
                logging.debug("Timeout: reenvio de paquete HELLO...")
            else:
                logging.info("No se pudo establecer la conexion")
                return (False, None)
    return (True, serverAddres)


def responder_conexion(socket, address, tipo_mensaje):
    for i in range(0, INTENTOS_CONEXION):
        enviar_hello_response(socket, address, tipo_mensaje)
        socket.settimeout(TIMEOUT_SEGUNDOS)
        try:
            pkg, clientAddres = socket.recvfrom(2048)
            logging.debug("Paquete recibido")
            msg = Traductor.paquete_a_mensaje(pkg, False)

            if msg.tipo_mensaje != TipoMensaje.HOLA_ACK:
                continue

            socket.settimeout(None)
            logging.debug("Paquete HELLO ACK recibido")
            break
        except TimeoutError:
            if i < INTENTOS_CONEXION - 1:
                logging.debug("Timeout: reenvio de paquete HELLO RESPONSE...")
            else:
                logging.info("No se pudo establecer la conexion")
                return False
    return True


def enviar_hello(socket, address, filename, tipo_mensaje):
    logging.debug("Enviando paquete HELLO...")
    tipo = TipoMensaje.HOLA + tipo_mensaje
    msg = Mensaje(tipo, 1, 1, filename)
    pkg = Traductor.MensajeAPaquete(msg)
    socket.sendto(pkg, address)


def enviar_hello_response(socket, address, tipo_mensaje):
    logging.debug("Enviando paquete HELLO RESPONSE...")
    tipo = TipoMensaje.HOLA + tipo_mensaje
    msg = Mensaje(tipo, 1, 1, None)
    pkg = Traductor.MensajeAPaquete(msg)
    socket.sendto(pkg, address)


def enviar_hello_ack(socket, address):
    logging.debug("Enviando paquete HELLO ACK...")
    tipo = TipoMensaje.HOLA_ACK + TipoMensaje.DOWNLOAD
    msg_hello_ack = Mensaje(tipo, 1, 1, None)
    pkg_hello_ack = Traductor.MensajeAPaquete(msg_hello_ack)
    socket.sendto(pkg_hello_ack, address)

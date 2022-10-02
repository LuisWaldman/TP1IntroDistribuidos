import logging
from _socket import timeout

from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.desfragmentador import Desfragmentador
from src.utils.Traductor import Traductor

class Receptor:
    MAX_PAYLOAD = 64000
    MAX_INTENTOS_CHAU = 5

    def __init__(self, socket, file_path):
        self.file_path = file_path
        self.socket = socket
        self.package_esperado = 1

    def recibir_archivo(self):
        termino_archivo = False

        with open(self.file_path, "wb") as file_destino:
            desfragmentador = Desfragmentador(file_destino, self.MAX_PAYLOAD)

            while not termino_archivo:
                logging.debug("Esperando paquete...")
                paquete_recibido, serverAddress = self.socket.recvfrom(64010) # todo hace cte (? o traer de archivo conf
                logging.debug("Paquete recibido")
                mensaje_recibido = Traductor.PaqueteAMensaje(
                    paquete_recibido,
                    False
                )

                logging.debug(f'package {mensaje_recibido.parte} | data size: {len(mensaje_recibido.payload)}')

                if mensaje_recibido.tipo_mensaje == TipoMensaje.ERROR:
                    logging.info("Error descargando parte: " + str(mensaje_recibido.parte))
                    return

                if not (mensaje_recibido.tipo_mensaje == TipoMensaje.PARTE and mensaje_recibido.parte == self.package_esperado):
                    logging.debug("Descartado parte no esperada: ")
                    return

                self.package_esperado += 1

                aux = desfragmentador.set_bytes_to_file(
                    mensaje_recibido.payload,
                    mensaje_recibido.parte
                )
                logging.debug(f"Bytes Escritos: {aux}")

                tipo = TipoMensaje.ACK +\
                    mensaje_recibido.tipo_operacion
                mensaje_ack = Mensaje(
                    tipo,
                    mensaje_recibido.total_partes,
                    mensaje_recibido.parte,
                    None
                )

                paquete_ack = Traductor.MensajeAPaquete(mensaje_ack)
                logging.debug(f"Envia ACK parte {mensaje_recibido.parte}")
                self.socket.sendto(paquete_ack, serverAddress)
                if mensaje_recibido.parte == mensaje_recibido.total_partes:
                    termino_archivo = True
                return serverAddress

    def esperar_cierre_conexion(self, direccion):
        closed = False
        intento = 0
        while not closed and intento < self.MAX_INTENTOS_CHAU:
            logging.info(
                "Esperando cierre de conexión (intento: "
                f"{intento}/{self.MAX_INTENTOS_CHAU})..."
            )
            try:
                paquete_recibido, __ = self.socket.recvfrom(64010)
                mensaje_recibido = Traductor.PaqueteAMensaje(
                    paquete_recibido,
                    False
                )
                if mensaje_recibido.tipo == TipoMensaje.CHAU:
                    logging.info("Cierre de conexión recibido.")
                    closed = True
                    logging.debug("Enviando ACK...")
                    msg = Mensaje(TipoMensaje.ACK, 0, 0, "")
                    pkg = Traductor.MensajeAPaquete(msg)
                    self.socket.sendto(pkg, direccion)
                else:
                    logging.debug(
                        f"El tipo de mensaje {mensaje_recibido.tipo} "
                        "recibido no fue CHAU."
                    )
                    intento = intento + 1
            except timeout:
                intento = intento + 1
import logging
from _socket import timeout

from src.conexion import Conexion
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.desfragmentador import Desfragmentador
from src.utils.Traductor import Traductor


class Receptor:
    MAX_PAYLOAD = 64000
    MAX_INTENTOS_CHAU = 5
    TIMEOUT_RECEPTOR = 30

    def __init__(self, socket, file_path):
        self.file_path = file_path
        self.socket = socket
        self.package_esperado = 1
        self.socket.settimeout(self.TIMEOUT_RECEPTOR)

    def recibir_archivo(self):
        conectado = True
        termino_archivo = False

        logging.debug("Abriendo archivo en path " + self.file_path)
        with open(self.file_path, "wb") as file_destino:
            desfragmentador = Desfragmentador(file_destino, self.MAX_PAYLOAD)

            while conectado:
                logging.debug("Esperando paquete...")
                try:
                    paquete_recibido, serverAddress = self.socket.recvfrom(64010)  # todo hace cte (? o traer de archivo conf
                except timeout:
                    raise Exception('Conexión interrumpida. No se reciben nuevos paquetes')
                    return

                logging.debug("Paquete recibido")
                mensaje_recibido = Traductor.paquete_a_mensaje(
                    paquete_recibido,
                    False
                )

                logging.debug(f'package {mensaje_recibido.parte} | data size: {len(mensaje_recibido.payload)}')

                if mensaje_recibido.tipo_mensaje == TipoMensaje.ERROR:
                    logging.info("Error descargando parte: " + str(mensaje_recibido.parte))
                    return

                if mensaje_recibido.tipo_mensaje == TipoMensaje.HOLA:
                    logging.info("Mensaje HELLO RESPONSE recibido")
                    self.reiniciar_transferencia(serverAddress)
                    continue

                if mensaje_recibido.tipo_mensaje == TipoMensaje.CHAU and termino_archivo:
                    self.cierre_conexion_ack(serverAddress)
                    conectado = False
                    continue

                elif not (mensaje_recibido.tipo_mensaje == TipoMensaje.PARTE and mensaje_recibido.parte <= self.package_esperado):
                    logging.debug("Descartado parte no esperada")
                    continue

                if mensaje_recibido.parte == self.package_esperado:
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

                paquete_ack = Traductor.mensaje_a_paquete(mensaje_ack)
                logging.debug(f"Envia ACK parte {mensaje_recibido.parte}")
                self.socket.sendto(paquete_ack, serverAddress)
                if mensaje_recibido.parte == mensaje_recibido.total_partes:
                    termino_archivo = True

    def reiniciar_transferencia(self, direccion):
        logging.info("Reiniciando tranferencia de archivo")
        self.package_esperado = 1
        Conexion.enviar_hello_ack(self.socket, direccion)

    def cierre_conexion_ack(self, direccion):
        logging.info("Cierre de conexión recibido.")
        logging.debug("Enviando ACK...")
        msg = Mensaje(TipoMensaje.ACK, 0, 0, None)
        pkg = Traductor.mensaje_a_paquete(msg)
        self.socket.sendto(pkg, direccion)
        logging.debug("Comunicación terminada")

import math
import logging
import threading
import time

from _socket import timeout
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.Traductor import Traductor

class Emisor:
    N = 3
    MAX_PAYLOAD = 64000
    MAX_REENVIOS_SEGUIDOS = 20
    MAX_INTENTOS_CHAU = 5

    def __init__(self, socket, file_path, direccion):
        self.file_path = file_path
        self.direccion = direccion
        self.socket = socket
        self.socket.settimeout(2) # segundos
        self.lock = threading.Lock()
        self.package = 1
        self.ack_esperado = 1
        self.timeout = False
        self.reenvios_seguidos = 0
        self.en_vuelo = 0


    def enviar_mensaje(self, frag, num_packages):
        self.lock.acquire()
        if self.en_vuelo < self.N and self.package <= num_packages:
            logging.debug(f"Enviando paquete numero {self.package}")
            data = frag.get_bytes_from_file(self.package)
            tipo = TipoMensaje.PARTE + TipoMensaje.DOWNLOAD
            logging.debug(f'package {self.package} data size: {len(data)}')
            msg = Mensaje(tipo, num_packages, self.package, data)
            pkg = Traductor.MensajeAPaquete(msg)
            # logging.debug("Contenido del mensaje: " + str(msg))
            self.socket.sendto(pkg, self.direccion)
            self.en_vuelo += 1
            self.package += 1
        else:
            self.lock.release()
            return

        self.lock.release()

        try:
            message, clientAddress = self.socket.recvfrom(2048)
        except timeout:
            self.lock.acquire()
            logging.debug(f'Timeout paquete {self.ack_esperado}')
            self.package = self.ack_esperado
            self.en_vuelo = 0
            self.reenvios_seguidos += 1
            self.lock.release()
            return

        self.lock.acquire()
        mensaje = Traductor.PaqueteAMensaje(message, False)
        if mensaje.tipo_mensaje == TipoMensaje.ACK and self.ack_esperado == mensaje.parte:
            logging.debug(f"Recibi el ack del paquete {mensaje.parte}")
            self.ack_esperado += 1
            self.en_vuelo -= 1
            self.reenvios_seguidos = 0
        self.lock.release()


    def enviar_archivo(self):
        with open(self.file_path, "rb") as file_origen:
            frag = Fragmentador(file_origen, self.MAX_PAYLOAD)
            total_size = frag.get_total_size()
            num_packages = math.ceil(total_size / self.MAX_PAYLOAD)

            logging.debug(f"Tamanio archivo: {total_size} bytes.")
            logging.debug(
                f"Enviando {num_packages} paquetes de {self.MAX_PAYLOAD} bytes"
            )

            hilos_hijos = list()
            while num_packages >= self.ack_esperado:
                if self.reenvios_seguidos > self.MAX_REENVIOS_SEGUIDOS:
                    logging.info('Conexión interrumpida. Máximo de reenvios alcanzado')
                    for hilo in hilos_hijos:
                        hilo.join()
                    return

                #logging.debug(f'Paquetes en vuelo: {self.en_vuelo} | Prox. paquete a enviar: {self.package} | Total de paquetes: {num_packages}')
                elif self.en_vuelo < self.N and self.package <= num_packages:
                    hilo = threading.Thread(
                        target=self.enviar_mensaje,
                        args=(frag, num_packages)
                    )
                    hilos_hijos.append(hilo)
                    hilo.start()

            logging.info('archivo enviado exitosamente')

    def cerrar_conexion(self):
        logging.info("Enviando mensaje CHAU...")
        conexion_cerrada = False
        intento = 0
        while not conexion_cerrada and intento < self.MAX_INTENTOS_CHAU:
            logging.info(
                "Enviando mensaje CHAU (intento: "
                f"{intento}/{self.MAX_INTENTOS_CHAU})..."
            )
            msg = Mensaje(TipoMensaje.CHAU, 0, 0, "")
            pkg = Traductor.MensajeAPaquete(msg)
            self.socket.sendto(pkg, self.direccion)
            logging.info("Mensaje CHAU enviado.")
            logging.info("Esperando ACK...")
            try:
                paquete_recibido, __ = self.socket.recvfrom(64010)
                mensaje_recibido = Traductor.PaqueteAMensaje(
                    paquete_recibido,
                    False
                )
                if mensaje_recibido.tipo == TipoMensaje.ACK:
                    conexion_cerrada = True
                    logging.info("ACK recibido. Conexion cerrada")
                else:
                    logging.debug(
                        f"El tipo de mensaje {mensaje_recibido.tipo} "
                        "recibido no fue CHAU."
                    )
                    intento = intento + 1
            except timeout:
                intento = intento + 1

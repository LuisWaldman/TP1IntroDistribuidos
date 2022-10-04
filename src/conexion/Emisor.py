import math
import logging
import threading

from _socket import timeout

from src.conexion import Conexion
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.Traductor import Traductor

class Emisor:
    MAX_PAYLOAD = 64000
    MAX_REENVIOS_SEGUIDOS = 30
    MAX_INTENTOS_CHAU = 5
    TIMEOUT = 0.25

    def __init__(self, socket, file_path, direccion, protocolo_N):
        self.file_path = file_path
        self.direccion = direccion
        self.socket = socket
        self.socket.settimeout(self.TIMEOUT)  # segundos
        self.lock = threading.Lock()
        self.package = 1
        self.ack_esperado = 1
        self.reenvios_seguidos = 0
        self.conexion_perdida = False
        self.N = protocolo_N
        self.en_vuelo = 0

    def enviar_paquetes(self, frag, num_packages):
        while self.ack_esperado <= num_packages:
            self.lock.acquire()
            if self.package <= num_packages and self.ack_esperado <= num_packages and (0 < (self.N - self.en_vuelo) <= self.N):
                self.en_vuelo += 1
                aux_package = self.package
                self.package += 1
                data = frag.get_bytes_from_file(aux_package)
                self.lock.release()

                logging.debug(f"Enviando paquete numero {aux_package}")
                tipo = TipoMensaje.PARTE + TipoMensaje.DOWNLOAD
                msg = Mensaje(tipo, num_packages, aux_package, data)
                pkg = Traductor.MensajeAPaquete(msg)
                self.socket.sendto(pkg, self.direccion)
                continue
            self.lock.release()

            if self.conexion_perdida:
                return

    def recibir_acks(self):
        if self.reenvios_seguidos > self.MAX_REENVIOS_SEGUIDOS:
            self.conexion_perdida = True
            return

        try:
            message, direccion = self.socket.recvfrom(2048)
        except timeout:
            logging.debug(f'Timeout paquete {self.ack_esperado}')
            self.lock.acquire()
            self.en_vuelo = 0
            self.package = self.ack_esperado
            self.lock.release()
            self.reenvios_seguidos += 1
            return

        mensaje = Traductor.paquete_a_mensaje(message, False)
        if mensaje.tipo_mensaje == TipoMensaje.ACK and mensaje.parte >= self.ack_esperado:
            logging.debug(f"Recibi el ack del paquete {mensaje.parte}")
            self.lock.acquire()
            self.ack_esperado = mensaje.parte + 1
            self.en_vuelo -= 1
            self.lock.release()
            self.reenvios_seguidos = 0
        elif mensaje.tipo_mensaje == TipoMensaje.HOLA:
            self.reiniciar_transferencia(direccion)

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
            for i in range(self.N):
                hilo = threading.Thread(
                    target=self.enviar_paquetes,
                    args=(frag, num_packages)
                )
                hilos_hijos.append(hilo)
                hilo.start()

            while self.ack_esperado <= num_packages and not self.conexion_perdida:
                self.recibir_acks()

            for hilo in hilos_hijos:
                hilo.join()

            if self.conexion_perdida:
                logging.info('Conexión interrumpida. Máximo de reenvios alcanzado')
            else:
                logging.info('archivo enviado exitosamente')
            self.cerrar_conexion()

    def reiniciar_transferencia(self, direccion):
        logging.info("Reiniciando tranferencia de archivo")
        self.package = 1
        self.ack_esperado = 1
        self.reenvios_seguidos = 0
        self.en_vuelo = 0
        Conexion.enviar_hello_ack(self.socket, direccion)

    def cerrar_conexion(self):
        if self.conexion_perdida:
            logging.debug("No se envía mensaje CHAU. Conexión perdida.")
            return
        conexion_cerrada = False
        intento = 1
        while not conexion_cerrada and intento <= self.MAX_INTENTOS_CHAU:
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
                mensaje_recibido = Traductor.paquete_a_mensaje(
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

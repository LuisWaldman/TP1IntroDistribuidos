import math
import logging
import threading

from _socket import timeout

from src.conexion import Conexion
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.Traductor import Traductor


class Emisor:
    N = 5
    MAX_PAYLOAD = 64000
    MAX_REENVIOS_SEGUIDOS = 30
    MAX_INTENTOS_CHAU = 5

    def __init__(self, socket, file_path, direccion, protocolo_N):
        self.file_path = file_path
        self.direccion = direccion
        self.socket = socket
        self.socket.settimeout(2)  # segundos
        self.lock = threading.Lock()
        self.package = 1
        self.ack_esperado = 1
        self.reenvios_seguidos = 0
        self.reinicio = False
        self.N = protocolo_N

    def enviar_mensajes(self, frag, num_packages):
        while self.package <= num_packages and self.ack_esperado <= num_packages:
            self.lock.acquire()
            package_aux = self.package
            self.package += 1
            self.lock.release()

            if self.reenvios_seguidos > self.MAX_REENVIOS_SEGUIDOS:
                break

            logging.debug(f"Enviando paquete numero {package_aux}")
            data = frag.get_bytes_from_file(package_aux)
            tipo = TipoMensaje.PARTE + TipoMensaje.DOWNLOAD
            logging.debug(f'package {package_aux} data size: {len(data)}')
            msg = Mensaje(tipo, num_packages, package_aux, data)
            pkg = Traductor.MensajeAPaquete(msg)
            self.socket.sendto(pkg, self.direccion)

            try:
                message, direccion = self.socket.recvfrom(2048)
            except timeout:
                logging.debug(f'Timeout paquete {self.ack_esperado}')
                if self.reinicio:
                    break

                if package_aux >= self.ack_esperado:
                    self.lock.acquire()
                    self.package = self.ack_esperado
                    self.reenvios_seguidos += 1
                    self.lock.release()
                continue

            mensaje = Traductor.PaqueteAMensaje(message, False)
            if mensaje.tipo_mensaje == TipoMensaje.ACK and mensaje.parte >= self.ack_esperado:
                logging.debug(f"Recibi el ack del paquete {mensaje.parte}")
                self.lock.acquire()
                self.ack_esperado = mensaje.parte + 1
                self.reenvios_seguidos = 0
                self.lock.release()
            elif mensaje.tipo_mensaje == TipoMensaje.HOLA:
                self.reinicio = True
                break

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
                    target=self.enviar_mensajes,
                    args=(frag, num_packages)
                )
                hilos_hijos.append(hilo)
                hilo.start()

            for hilo in hilos_hijos:
                hilo.join()

            if self.reinicio:
                self.reiniciar_transferencia(self.direccion)

            if self.reenvios_seguidos > self.MAX_REENVIOS_SEGUIDOS:
                logging.info('Conexión interrumpida. Máximo de reenvios alcanzado')
                return

            logging.info('archivo enviado exitosamente')

    def reiniciar_transferencia(self, direccion):
        logging.info("Reiniciando tranferencia de archivo")
        self.package = 1
        self.ack_esperado = 1
        self.reenvios_seguidos = 0
        self.reinicio = False
        Conexion.enviar_hello_ack(self.socket, direccion)

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

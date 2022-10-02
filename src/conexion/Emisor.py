import math
import logging
import threading

from _socket import timeout
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.Traductor import Traductor

class Emisor:
    N = 3
    MAX_PAYLOAD = 64000

    def __init__(self, socket, file_path, direccion):
        self.file_path = file_path
        self.direccion = direccion
        self.socket = socket
        self.socket.settimeout(5) # segundos
        self.lock = threading.Lock()
        self.package = 1
        self.ack_esperado = 1
        self.timeout = False
        self.en_vuelo = 0


    def enviar_mensaje(self, frag, num_packages):
        self.lock.acquire()
        if self.en_vuelo < self.N and self.package <= num_packages:
            logging.info(f"Enviando paquete numero {self.package}")
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
            self.timeout = True
            return

        self.lock.acquire()
        mensaje = Traductor.PaqueteAMensaje(message, False)
        if mensaje.tipo_mensaje == TipoMensaje.ACK and self.ack_esperado == mensaje.parte:
            logging.info(f"Recibi el ack del paquete {mensaje.parte}")
            self.ack_esperado += 1
            self.en_vuelo -= 1
        self.lock.release()


    def enviar_archivo(self):
        with open(self.file_path, "rb") as file_origen:
            frag = Fragmentador(file_origen, self.MAX_PAYLOAD)
            total_size = frag.get_total_size()
            num_packages = math.ceil(total_size / self.MAX_PAYLOAD)

            logging.info(f"Tamanio archivo: {total_size} bytes.")
            logging.info(
                f"Enviando {num_packages} paquetes de {self.MAX_PAYLOAD} bytes"
            )

            hilos_hijos = list() # todo ver esto si lo sacamos o no
            while num_packages >= self.ack_esperado:
                if self.timeout:
                    logging.info(f'Timeout paquete {self.ack_esperado}')
                    self.timeout = False
                    self.package = self.ack_esperado

                #logging.debug(f'Paquetes en vuelo: {self.en_vuelo} | Prox. paquete a enviar: {self.package} | Total de paquetes: {num_packages}')
                if self.en_vuelo < self.N and self.package <= num_packages:
                    hilo = threading.Thread(
                        target=self.enviar_mensaje,
                        args=(frag, num_packages)
                    )
                    hilos_hijos.append(hilo)
                    hilo.start()

            logging.info('archivo enviado exitosamente')
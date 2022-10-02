import math
import logging

from _socket import timeout
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.Traductor import Traductor
import threading
import time

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


    def enviar_mensaje(self, frag, num_packages):
        self.lock.acquire()
        logging.info(f"Enviando paquete numero {self.package}")
        data = frag.get_bytes_from_file(self.package)
        tipo = TipoMensaje.PARTE + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
        msg = Mensaje(tipo, num_packages, self.package, data)
        pkg = Traductor.MensajeAPaquete(msg)
        logging.debug("Contenido del mensaje: " + str(msg))
        self.socket.sendto(pkg, self.direccion)
        self.package += 1
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

            hilos_hijos = list()
            while num_packages >= self.ack_esperado:
                for i in range(self.N):
                    if self.package <= num_packages:
                        hilo = threading.Thread(
                            target=self.enviar_mensaje,
                            args=(frag, num_packages)
                        )
                        hilos_hijos.append(hilo)
                        hilo.start()

                # TODO: No es una buena idea hacer sleep para sincronizar
                time.sleep(5)
                for hilo in hilos_hijos:
                    # TODO: pensar que si ya uno devuelven bien que envie otro
                    # TODO: tener algun tipo de contador de vacantes para enviar
                    hilo.join()
                if self.timeout:
                    logging.info(f'Timeout paquete {self.ack_esperado}')
                    self.timeout = False
                    self.package = self.ack_esperado

            logging.info('archivo enviado exitosamente')
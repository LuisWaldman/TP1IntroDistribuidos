import math
from _socket import timeout
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.fragmentador import Fragmentador
from src.utils.salida import Salida
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
        Salida.info(f"Enviamos el paquete {self.package}")
        data = frag.get_bytes_from_file(self.package)
        tipo = TipoMensaje.PARTE + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
        msg = Mensaje(tipo, num_packages, self.package, data)
        pkg = Traductor.MensajeAPaquete(msg)
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
            Salida.info(f"Recibi el ack del paquete {mensaje.parte}")
            self.ack_esperado += 1
        self.lock.release()


    def enviar_archivo(self):
        with open(self.file_path, "rb") as file_origen:
            frag = Fragmentador(file_origen, self.MAX_PAYLOAD)
            total_size = frag.get_total_size()
            num_packages = math.ceil(total_size / self.MAX_PAYLOAD)

            Salida.info(f"Arch origen: {total_size}bytes.")
            Salida.info(f"Se necesita {num_packages} paq de {self.MAX_PAYLOAD} bytes.\n")

            hilos_hijos = list()
            while num_packages >= self.ack_esperado:
                for i in range(self.N):
                    if self.package <= num_packages:
                        hilo = threading.Thread(target=self.enviar_mensaje,
                                                args=(frag, num_packages))
                        hilos_hijos.append(hilo)
                        hilo.start()

                time.sleep(5)
                for hilo in hilos_hijos: # todo pensar que si ya uno devuelven bien que envie otro
                                        # todo tener algun tipo de contador de vacantes para enviar
                    hilo.join()
                if self.timeout:
                    Salida.info(f'Timeout paquete {self.ack_esperado}')
                    self.timeout = False
                    self.package = self.ack_esperado

            Salida.info('archivo enviado exitosamente')
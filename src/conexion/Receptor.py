import math
from _socket import timeout
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.desfragmentador import Desfragmentador
from src.utils.fragmentador import Fragmentador
from src.utils.salida import Salida
from src.utils.Traductor import Traductor
import threading

class Receptor:
    MAX_PAYLOAD = 64000

    def __init__(self, socket, file_path):
        self.file_path = file_path
        self.socket = socket
        self.package_esperado = 1


    def recibir_archivo(self):
        termino_archivo = False

        with open(self.file_path, "wb") as file_destino:
            desfragmentador = Desfragmentador(file_destino, self.MAX_PAYLOAD)

            while not termino_archivo:
                Salida.verborragica("Esperando paquete...")
                paquete_recibido, serverAddress = self.socket.recvfrom(2048)
                Salida.verborragica("Paquete recibido")
                mensaje_recibido = Traductor.PaqueteAMensaje(
                    paquete_recibido,
                    False
                )
                if mensaje_recibido.tipo_mensaje == TipoMensaje.ERROR:
                    Salida.info("Error descargando parte: " + mensaje_recibido.payload)
                    return

                aux = desfragmentador.set_bytes_to_file(
                    mensaje_recibido.payload,
                    mensaje_recibido.parte
                )
                Salida.verborragica(f"Bytes Escritos: {aux}")

                tipo = TipoMensaje.ACK +\
                    mensaje_recibido.tipo_operacion +\
                    mensaje_recibido.tipo_protocolo
                mensaje_ack = Mensaje(
                    tipo,
                    mensaje_recibido.total_partes,
                    mensaje_recibido.parte,
                    None
                )
                paquete_ack = Traductor.MensajeAPaquete(mensaje_ack)
                Salida.verborragica(f"Envia ACK parte {mensaje_recibido.parte}")
                self.socket.sendto(paquete_ack, serverAddress)
                if mensaje_recibido.parte == mensaje_recibido.total_partes:
                    termino_archivo = True

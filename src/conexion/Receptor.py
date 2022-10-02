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
        terminoarhivo = False

        with open(self.file_path, "wb") as file_destino:
            desfrag = Desfragmentador(file_destino, self.MAX_PAYLOAD)

            while not terminoarhivo:
                Salida.verborragica("esperando paquete ...")
                paqueterecibido, serverAddress = self.socket.recvfrom(2048)
                Salida.verborragica("paquete recibido")
                mensajerecibido = Traductor.PaqueteAMensaje(paqueterecibido, False)

                aux = desfrag.set_bytes_to_file(mensajerecibido.payload,
                                                mensajerecibido.parte)
                Salida.verborragica(f"Bytes Escritos: {aux}")

                tipo = TipoMensaje.ACK + mensajerecibido.tipo_operacion + mensajerecibido.tipo_protocolo
                mensajeAck = Mensaje(tipo, mensajerecibido.total_partes, mensajerecibido.parte, None)
                paqueteack = Traductor.MensajeAPaquete(mensajeAck)
                Salida.verborragica(f"Envia ACK parte {mensajerecibido.parte}")
                self.socket.sendto(paqueteack, serverAddress)
                if mensajerecibido.parte == mensajerecibido.total_partes:
                    terminoarhivo = True

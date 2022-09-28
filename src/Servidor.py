import socket
from .Hilo import Hilo

class Servidor:
    BUFER_MAXIMO = 1024

    def __init__(self, ip, puerto):
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conexion.bind((ip, puerto))

    def escuchar(self):
        while True:
            mensaje, direccion = self.conexion.recvfrom(self.BUFER_MAXIMO)
            hilo = Hilo(mensaje)
            hilo.iniciar()

import socket


class Cliente:
    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def enviar_mensaje(self, mensaje):
        self.conexion.sendto(mensaje, (self.ip, self.puerto))

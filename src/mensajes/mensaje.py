import enum


class TipoMensaje(enum.IntEnum):
    NODEFINIDO = 0
    HOLA = 1
    CHAU = 2
    PARTE = 3
    ACK = 4
    ERROR = 5

    # Operacion
    DOWNLOAD = 10
    UPLOAD = 20

    # Protocolo
    STOPANDWAIT = 100
    GBN = 200


class Mensaje:
    tipo = TipoMensaje.NODEFINIDO
    total_partes = 0
    parte = 0
    tamanio_payload = 0
    payload = ""

    tipo_mensaje = 0
    tipo_operacion = 0
    tipo_protocolo = 0

    def __init__(self, tipo_msg, total_partes, parte, payload):
        self.tipo = tipo_msg
        self.total_partes = total_partes
        self.parte = parte
        self.payload = payload
        self.tamanio_payload = len(payload) if payload != None else 0
        if (tipo_msg > 9):
            self.extraer_tipo(tipo_msg)

    def extraer_tipo(self, mensaje):
        mensaje_str = str(mensaje)
        self.tipo_mensaje = int(mensaje_str[-1])
        if len(mensaje_str) > 1:
            self.tipo_operacion = int(mensaje_str[-2]) * 10
        if len(mensaje_str) > 2:
            self.tipo_protocolo = int(mensaje_str[-3]) * 100

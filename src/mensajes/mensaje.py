import enum


class TipoMensaje(enum.IntEnum):
    NODEFINIDO = 0
    HOLA = 1
    CHAU = 2
    PARTE = 3
    ACK = 4
    ERROR = 5
    OBTENERLISTADO = 6

    # Operacion
    DOWNLOAD = 10
    UPLOAD = 20


class Mensaje:
    tipo = TipoMensaje.NODEFINIDO
    total_partes = 0
    parte = 0
    tamanio_payload = 0
    payload = ""

    tipo_mensaje = 0
    tipo_operacion = 0

    def __init__(self, tipo_msg, total_partes, parte, payload):
        self.tipo = tipo_msg
        self.total_partes = total_partes
        self.parte = parte
        self.payload = payload
        self.tamanio_payload = len(payload) if payload != None else 0
        if (tipo_msg > 9):
            self.extraer_tipo(tipo_msg)
        else:
            self.tipo_mensaje = tipo_msg

    def __str__(self):
        return f"Tipo: {TipoMensaje(self.tipo_mensaje).name} " +\
            f"Tipo operacion: {TipoMensaje(self.tipo_operacion).name} " +\
            f"Total partes: {self.total_partes} Parte: {self.parte} " +\
            f"Tamanio payload: {self.tamanio_payload} Payload: {self.payload}"

    def extraer_tipo(self, mensaje):
        mensaje_str = str(mensaje)
        self.tipo_mensaje = int(mensaje_str[-1])
        if len(mensaje_str) > 1:
            self.tipo_operacion = int(mensaje_str[-2]) * 10

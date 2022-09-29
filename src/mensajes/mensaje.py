import enum

class EnumOperacion(enum.Enum):
    DOWNLOAD = 1
    UPLOAD = 2

class EnumProtocolo(enum.Enum):
    STOPANDWAIT = 1
    GBN = 2

class Mensaje:
    nombre = ""

class Mensaje_hola(Mensaje):
    operacion = EnumOperacion.UPLOAD
    protocolo = EnumProtocolo.GBN

    def __init__(self, p_operacion, p_protocolo):
        self.nombre = "HOLA"
        self.operacion = p_operacion
        self.protocolo = p_protocolo


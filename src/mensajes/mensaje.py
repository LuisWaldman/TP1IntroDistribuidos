import enum


class TipoMensaje(enum.Enum):
    NODEFINIDO = 0
    HOLA = 1
    CHAU = 2
    ACK = 3
    ERROR = 4
class EnumOperacion(enum.Enum):
    DOWNLOAD = 1
    UPLOAD = 2

class EnumProtocolo(enum.Enum):
    STOPANDWAIT = 1
    GBN = 2

class Mensaje:
    tipo = TipoMensaje.NODEFINIDO

class Mensaje_hola(Mensaje):
    operacion = EnumOperacion.UPLOAD
    protocolo = EnumProtocolo.GBN

    def __init__(self, p_operacion, p_protocolo):
        self.tipo = TipoMensaje.HOLA
        self.operacion = p_operacion
        self.protocolo = p_protocolo


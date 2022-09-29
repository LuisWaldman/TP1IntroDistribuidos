import enum


class TipoMensaje(enum.Enum):
    NODEFINIDO = 0
    HOLA = 1
    CHAU = 2
    PARTE = 3
    ACK = 4
    ERROR = 5
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
    archivo = ""

    def __init__(self, p_operacion, p_protocolo, p_archivo):
        self.tipo = TipoMensaje.HOLA
        self.operacion = p_operacion
        self.protocolo = p_protocolo
        self.archivo = p_archivo



class Mensaje_parte(Mensaje):
    id_conexion = 0
    parte = 0
    totalpartes = 0


class Mensaje_ack(Mensaje):
    id_conexion = 0
    parte = 0
    totalpartes = 0

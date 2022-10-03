import enum
import hashlib


class TipoMensaje(enum.IntEnum):
    NODEFINIDO = 0
    HOLA = 1
    CHAU = 2
    PARTE = 3
    ACK = 4
    ERROR = 5
    OBTENERLISTADO = 6
    HOLA_ACK = 7

    # Operacion
    DOWNLOAD = 10
    UPLOAD = 20


class Mensaje:
    tipo = TipoMensaje.NODEFINIDO
    total_partes = 0
    parte = 0
    tamanio_payload = 0
    payload = ""
    checksum = 0
    checksum_complemento = 0

    tipo_mensaje = 0
    tipo_operacion = 0

    def __init__(self, tipo_msg, total_partes, parte, payload):
        self.tipo = tipo_msg
        self.total_partes = total_partes
        self.parte = parte
        self.payload = payload
        self.tamanio_payload = len(payload) if payload is not None else 0
        if (tipo_msg > 9):
            self.extraer_tipo(tipo_msg)
        else:
            self.tipo_mensaje = tipo_msg
        self.calcular_checksum()

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

    def calcular_checksum(self):
        sum = self.tipo + self.total_partes + self.parte + self.tamanio_payload
        if int(self.tamanio_payload) > 0:
            sum += self.calcular_sum_payload()

        checksum_binario = bin(sum)
        if len(checksum_binario) < 18:
            checksum_binario = '0000000000000000' + checksum_binario[2:]
        checksum_dos_bytes = checksum_binario[-16:]

        self.checksum = int(checksum_dos_bytes, 2)
        self.calcular_checksum_complemento(checksum_dos_bytes)

    def calcular_sum_payload(self):
        if type(self.payload) != type(b'abc123'):  # todo corregir esto: el fragmentador devuelve bytes no es necesario encodear en ese caso
            payload = self.payload.encode('utf-8')
        else:
            payload = self.payload

        h = hashlib.sha256()
        h.update(payload)
        payload_bytes = h.digest()
        bytes = []
        sum = 0

        for i in range(0, 16):
            bytes.append(int.from_bytes(payload_bytes[2 * i:2 * i + 2], byteorder='big'))
        for i in bytes:
            sum += i
        return sum

    def calcular_checksum_complemento(self, checksum_binario):
        complemento = ""
        for i in checksum_binario:
            if i == '1':
                complemento += '0'
            else:
                complemento += '1'
        self.checksum_complemento = int(complemento, 2)

from src.mensajes.mensaje import Mensaje, TipoMensaje


TAMANIO_BYTE = 256
SUM_CHECKSUM = 65535


class Traductor:
    @staticmethod
    def MensajeAPaquete(mensaje):
        # Cabecera
        tipo_msg = int(mensaje.tipo).to_bytes(1, byteorder='big', signed=False)
        total_partes = int(mensaje.total_partes) \
            .to_bytes(1, byteorder='big', signed=False)
        parte = int(mensaje.parte) \
            .to_bytes(1, byteorder='big', signed=False)
        tamanio_payload = int(mensaje.tamanio_payload) \
            .to_bytes(2, byteorder='big', signed=False)
        checksum = int(mensaje.checksum_complemento) \
            .to_bytes(2, byteorder='big', signed=False)

        # Payload MAX 64 KB
        if not isinstance(mensaje.payload, bytes):
            payload = mensaje.payload.encode('utf-8') if int(mensaje.tamanio_payload) > 0 else None
        else:
            payload = mensaje.payload if int(mensaje.tamanio_payload) > 0 else None

        return tipo_msg + total_partes + parte + tamanio_payload + checksum + payload if int(mensaje.tamanio_payload) > 0 \
            else tipo_msg + total_partes + parte + tamanio_payload + checksum

    @staticmethod
    def paquete_a_mensaje(bytes, convertir_string):
        # Cabecera
        tipo_msg = bytes[0]
        total_partes = bytes[1]
        parte = bytes[2]
        tamanio_payload = bytes[3] * TAMANIO_BYTE + bytes[4]
        checksum = bytes[5] * TAMANIO_BYTE + bytes[6]

        # Payload MAX 64 KB
        if convertir_string:
            payload = bytes[7:tamanio_payload + 7].decode('utf-8')
        else:
            payload = bytes[7:tamanio_payload + 7]

        mensaje = Mensaje(tipo_msg, total_partes, parte, payload)
        if checksum + mensaje.checksum != SUM_CHECKSUM:
            return Mensaje(TipoMensaje.ERROR, total_partes, parte, "Checksum difiere")
        return mensaje

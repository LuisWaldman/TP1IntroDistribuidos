from src.mensajes.mensaje import Mensaje

TAMANIO_BYTE = 256


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

        # Payload MAX 64 KB
        if type(mensaje.payload) != type(b'abc123'): # todo corregir esto: el fragmentador devuelve bytes no es necesario encodear en ese caso
            payload = mensaje.payload.encode('utf-8') if int(mensaje.tamanio_payload) > 0 else None
        else:
            payload = mensaje.payload if int(mensaje.tamanio_payload) > 0 else None

        return tipo_msg + total_partes + parte + tamanio_payload + payload if int(mensaje.tamanio_payload) > 0 else tipo_msg + total_partes + parte + tamanio_payload

    @staticmethod
    def PaqueteAMensaje(bytes, convertir_string):
        # Cabecera
        tipo_msg = bytes[0]
        total_partes = bytes[1]
        parte = bytes[2]
        tamanio_payload = bytes[3] * TAMANIO_BYTE + bytes[4]

        # Payload MAX 64 KB
        if convertir_string:
            payload = bytes[5:tamanio_payload+5].decode('utf-8')
        else:
            payload = bytes[5:tamanio_payload + 5]

        return Mensaje(tipo_msg, total_partes, parte, payload)

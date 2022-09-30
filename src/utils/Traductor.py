from mensajes.mensaje import Mensaje

TAMANIO_BYTE = 256


class Traductor:
    @staticmethod
    def MensajeAPaquete(mensaje):
        # Cabecera
        tipo_msg = int(mensaje.tipo).to_bytes(1, byteorder='big', signed=False)
        cantidad_de_partes = int(mensaje.cantidad_de_partes) \
            .to_bytes(1, byteorder='big', signed=False)
        parte_en_vuelo = int(mensaje.parte_en_vuelo) \
            .to_bytes(1, byteorder='big', signed=False)
        tamanio_playload = int(mensaje.tamanio_playload) \
            .to_bytes(2, byteorder='big', signed=False)

        # Playload MAX 64 KB
        playload = mensaje.playload.encode('utf-8')

        return tipo_msg + cantidad_de_partes + parte_en_vuelo + \
            tamanio_playload + playload

    @staticmethod
    def PaqueteAMensaje(bytes):
        # Cabecera
        tipo_msg = bytes[0]
        cantidad_de_partes = bytes[1]
        parte_en_vuelo = bytes[2]
        tamanio_playload = bytes[3] * TAMANIO_BYTE + bytes[4]

        # Playload MAX 64 KB
        playload = bytes[5:tamanio_playload+5].decode('utf-8')

        return Mensaje(tipo_msg, cantidad_de_partes, parte_en_vuelo, playload)

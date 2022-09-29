from mensajes.mensaje import *

class Traductor:
    @staticmethod
    def MensajeAPaquete(mensaje):
        ret = bytes()
        if (mensaje.tipo == TipoMensaje.HOLA):
            cabecera = str(int(mensaje.tipo.value)) + str(int(mensaje.operacion.value)) + str(int(mensaje.protocolo.value))
            ret = cabecera.encode()
        return ret

    @staticmethod
    def PaqueteAMensaje(byte):
        primercaracter = chr(byte[0])
        if (primercaracter == "1"):
            segundocaracter = chr(byte[1])
            tercercaracter = chr(byte[2])
            oper = EnumOperacion.DOWNLOAD
            prot = EnumProtocolo.STOPANDWAIT
            if segundocaracter == "2":
                oper = EnumOperacion.UPLOAD
            if tercercaracter == "2":
                prot = EnumProtocolo.GBN
            return Mensaje_hola(oper, prot)
        return Mensaje()

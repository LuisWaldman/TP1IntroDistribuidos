import enum


class EnumSalida(enum.Enum):
    NINGUNA = 1
    INFORMACION = 2
    VERBORRAGICA = 3


class Salida:

    enumsalida = EnumSalida.INFORMACION

    @staticmethod
    def info(mensaje):
        if Salida.enumsalida != EnumSalida.NINGUNA:
            print(mensaje)

    @staticmethod
    def verborragica(mensaje):
        if Salida.enumsalida == EnumSalida.VERBORRAGICA:
            print(mensaje)

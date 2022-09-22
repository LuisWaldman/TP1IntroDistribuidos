import enum


class EnumSalida(enum.Enum):
    NINGUNA = 1
    INFORMACION = 2
    VERBORRAGICA = 3


class Salida:
    enumsalida = EnumSalida.INFORMACION

    def __init__(self, penum_salida):
        self.enumsalida = penum_salida

    def info(self, mensaje):
        if self.enumsalida != EnumSalida.NINGUNA:
            print(mensaje)

    def verborragica(self, mensaje):
        if self.enumsalida == EnumSalida.VERBORRAGICA:
            print(mensaje)

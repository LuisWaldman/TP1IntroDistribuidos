import enum


class EnumSalida(enum.Enum):
    Ninguna = 1
    Informacion = 2
    Verborragica = 3


class Salida:
    enumsalida = EnumSalida.Informacion

    def __init__(self, penumSalida):
        self.enumsalida = penumSalida

    def Info(self, mensaje):
        if self.enumsalida != EnumSalida.Ninguna:
            print(mensaje)

    def Verborragica(self, mensaje):
        if self.enumsalida == EnumSalida.Verborragica:
            print(mensaje)

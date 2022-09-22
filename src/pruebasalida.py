from src.salida import Salida, EnumSalida


print("Ninguna")
salida = Salida(EnumSalida.NINGUNA)
salida.info("Info")
salida.verborragica("Verbo")

print("Informacion")
salida = Salida(EnumSalida.INFORMACION)
salida.info("Info")
salida.verborragica("Verbo")

print("Verborragica")
salida = Salida(EnumSalida.VERBORRAGICA)
salida.info("Info")
salida.verborragica("Verbo")

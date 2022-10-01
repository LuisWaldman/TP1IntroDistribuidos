from src.utils.salida import Salida, EnumSalida


print("Ninguna")
Salida.enumsalida = EnumSalida.NINGUNA
Salida.info("Info")
Salida.verborragica("Verbo")

print("Informacion")
Salida.enumsalida = EnumSalida.INFORMACION
Salida.info("Info")
Salida.verborragica("Verbo")

print("Verborragica")
Salida.enumsalida = EnumSalida.VERBORRAGICA
Salida.info("Info")
Salida.verborragica("Verbo")

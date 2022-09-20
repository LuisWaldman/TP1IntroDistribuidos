from salida import Salida, EnumSalida


print("Ninguna")
salida = Salida(EnumSalida.Ninguna)
salida.Info("Info")
salida.Verborragica("Verbo")

print("Informacion")
salida = Salida(EnumSalida.Informacion)
salida.Info("Info")
salida.Verborragica("Verbo")

print("Verborragica")
salida = Salida(EnumSalida.Verborragica)
salida.Info("Info")
salida.Verborragica("Verbo")

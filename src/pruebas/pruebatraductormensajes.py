from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor

tipo_msg = TipoMensaje.HOLA + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
cantidad_de_partes = 1
parte_en_vuelo = 1
playload = 'abcde'

mensaje = Mensaje(tipo_msg, cantidad_de_partes, parte_en_vuelo, playload)
paquete = Traductor.MensajeAPaquete(mensaje)
mensaje_retraducido = Traductor.PaqueteAMensaje(paquete)

assert mensaje_retraducido.tipo_mensaje == TipoMensaje.HOLA
assert mensaje_retraducido.tipo_operacion == TipoMensaje.DOWNLOAD
assert mensaje_retraducido.tipo_protocolo == TipoMensaje.STOPANDWAIT
assert mensaje_retraducido.cantidad_de_partes == cantidad_de_partes
assert mensaje_retraducido.parte_en_vuelo == parte_en_vuelo
assert mensaje_retraducido.playload == playload

from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor

mensaje_parte = Mensaje(TipoMensaje.PARTE, 1, 12, "ABCD")



tipo_msg = TipoMensaje.HOLA + TipoMensaje.DOWNLOAD + TipoMensaje.STOPANDWAIT
total_partes = 1
parte = 1
payload = 'abcde'

mensaje = Mensaje(tipo_msg, total_partes, parte, payload)
paquete = Traductor.MensajeAPaquete(mensaje)
mensaje_retraducido = Traductor.PaqueteAMensaje(paquete)

assert mensaje_retraducido.tipo_mensaje == TipoMensaje.HOLA
assert mensaje_retraducido.tipo_operacion == TipoMensaje.DOWNLOAD
assert mensaje_retraducido.tipo_protocolo == TipoMensaje.STOPANDWAIT
assert mensaje_retraducido.total_partes == total_partes
assert mensaje_retraducido.parte == parte
assert mensaje_retraducido.payload == payload

from src.mensajes.mensaje import *
from src.utils.Traductor import *

oper = EnumOperacion.DOWNLOAD
prot = EnumProtocolo.GBN

mensaje = Mensaje_hola(oper, prot)
paquete = Traductor.MensajeAPaquete(mensaje)
mensaje_retraducido = Traductor.PaqueteAMensaje(paquete);
assert mensaje_retraducido.tipo == TipoMensaje.HOLA
assert mensaje_retraducido.protocolo == prot
assert mensaje_retraducido.operacion == oper

import math
from src.utils.fragmentador import Fragmentador
from src.utils.desfragmentador import Desfragmentador
from src.mensajes.mensaje import TipoMensaje, Mensaje
from src.utils.Traductor import Traductor

def copiar_archivo():
    package = 1
    mss = 1000

    path_origen = 'meme1.jpg'
    path_destino = 'copiameme1.jpg'

    with open(path_origen, "rb") as file_origen:
        with open(path_destino, "wb") as file_destino:

            frag = Fragmentador(file_origen, mss)
            total_size = frag.get_total_size()
            num_packages = math.ceil(total_size/mss)
            print(f"Arch origen: {total_size}bytes.\n")
            print(f"Se necesita {num_packages} paq de mss {mss} bytes.\n")
            desfrag = Desfragmentador(file_destino, mss)

            while 0 < package <= num_packages:
                bytes_leidos = frag.get_bytes_from_file(package)
                print(f'largo del paquete {package} es : {len(bytes_leidos)}')

                mensajeparte = Mensaje(TipoMensaje.PARTE, num_packages, package, bytes_leidos)
                paqueteparte = Traductor.MensajeAPaquete(mensajeparte)
                mensaje_retraducido = Traductor.PaqueteAMensaje(paqueteparte)

                aux = desfrag.set_bytes_to_file(bytes_leidos, mensaje_retraducido.payload)
                print(f'Se escribieron {aux} bytes en {path_destino}\n')
                package = package + 1


if __name__ == '__main__':
    copiar_archivo()

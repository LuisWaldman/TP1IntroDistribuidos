from fragmentador import *
from desfragmentador import *
import math

def copiarArchivo():
    package = 1
    mss = 100

    pathOrigen = 'cliente.py'
    frag = Fragmentador(pathOrigen, mss)
    totalSize = frag.getTotalSize()
    numPackages = math.ceil(totalSize/mss)
    print(f"El archivo de origen es de {totalSize} bytes, por lo que se necesitarán {numPackages} paquetes de mss {mss} bytes para enviarlo completo.\n")

    pathDestino = 'nuevoArch.py'
    desfrag = Desfragmentador(pathDestino, frag.getTotalSize(), mss)

    while(package > 0 and package <= numPackages):
        bytesLeidos = frag.getBytesFromFile(package)
        print(f'largo del paquete {package} es : {len(bytesLeidos)}')
        aux = desfrag.setBytesToFile(bytesLeidos, package)
        print(f'Se escribieron {aux} bytes en el archivo {pathDestino}\n')
        package = package + 1

    frag.close()
    desfrag.close()


if __name__ == '__main__':
    copiarArchivo()
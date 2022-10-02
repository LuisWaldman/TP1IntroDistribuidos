import os

LEN_IP_ADDR = 4


class Parametros:
    mss = 5000

    mostrar_ayuda = False
    enum_salida = "INFO"
    ip = "localhost"
    port = 10666
    path = "/home/luis/repo/"
    filename = ""
    error = False

    def __init__(self, parametros):
        cargando = ""
        for par in parametros:
            if par == "-h":
                self.mostrar_ayuda = True
                cargando = ""
            elif par == "-v":
                self.enum_salida = "DEBUG"
                cargando = ""
            elif par == "-q":
                self.enum_salida = "WARN"
                cargando = ""
            elif par in ('-H', '-p', '-s', '-d', '-n'):
                cargando = par
            else:
                if cargando == "-H":
                    self.ip = par
                elif cargando == "-p":
                    self.port = int(par)
                elif cargando == "-s" or cargando == "-d":
                    self.path = par
                elif cargando == "-n":
                    self.filename = par

        self.validateIp()
        self.validatePort()
        self.validatePath()

    def validateIp(self):
        if self.ip == 'localhost':
            return
        numbers = self.ip.split('.')
        if len(numbers) != LEN_IP_ADDR:
            print('ERROR: IP address invalida')
            self.error = True
            return
        for number in numbers:
            if int(number) < 0 or int(number) > 255:
                print('ERROR: IP address invalida')
                self.error = True
                return

    def validatePort(self):
        if self.port < 1024 or self.port > 65535:
            print('ERROR: Puerto invalido')
            self.error = True

    def validatePath(self):
        if not os.path.isdir(self.path):
            print('ERROR: Ruta invalida')
            self.error = True

import threading


class Hilo:
    def __init__(self, mensaje = None):
        self.hilo = threading.Thread(target=self.tarea)
        self.mensaje = mensaje

    def agregar_mensaje(self, mensaje):
        self.mensaje = mensaje

    def tarea(self):
        print('Para Implementar')
        print(self.mensaje)

    def iniciar(self):
        self.hilo.setDaemon(True)
        self.hilo.start()

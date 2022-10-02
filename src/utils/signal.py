"""Signal handler."""

from src.utils.salida import Salida

def sigint_exit(signum, frame):
    """Terminate execution with 0 after receiving SIGINT."""
    Salida.info("Ctrl-c fue presionado. Saliendo...")
    exit(0)

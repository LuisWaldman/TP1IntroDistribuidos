"""Signal handler."""

import logging

def sigint_exit(signum, frame):
    """Terminate execution with 0 after receiving SIGINT."""
    logging.info("Ctrl-c fue presionado. Saliendo...")
    exit(0)

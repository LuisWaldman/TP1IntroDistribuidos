from logging import getLogger, getLevelName, Formatter, StreamHandler


def set_up_log(level):
    log = getLogger()
    log.setLevel(getLevelName(level))
    log_formatter = Formatter(
        "%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s"
    )
    console_handler = StreamHandler()
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)

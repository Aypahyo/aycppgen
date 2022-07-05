
from logging import DEBUG, Logger, StreamHandler, basicConfig, getLogger
import sys

def logginghelper_set_up_logs(level=DEBUG):
    logging_handlers = [StreamHandler(sys.stdout)]
    basicConfig(
        handlers=logging_handlers,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        level=level
    )

def logginghelper_getOrDefault(name : str, logger : Logger) -> Logger:
    rv = getLogger(name) if logger is None else logger
    if not isinstance(rv.handlers, list) or len(rv.handlers) == 0:
        print(f'logger for {name} is broken - improvising')
        rv.error = lambda msg :  print(f'{name} error {msg}')
        rv.debug = lambda msg :  print(f'{name} debug {msg}')
        rv.warn = lambda msg :  print(f'{name} warn {msg}')
        rv.info = lambda msg :  print(f'{name} info {msg}')
        rv.warning = lambda msg :  print(f'{name} warn {msg}')
        rv.critical = lambda msg :  print(f'{name} fatal {msg}')
    return rv

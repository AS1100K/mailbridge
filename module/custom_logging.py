import logging
import os
import sys


def getLogger(name='root', loglevel='INFO', logfile='app.log'):
    logger = logging.getLogger(name)

    # if logger 'name' already exists, return it to avoid logging duplicate
    # messages by attaching multiple handlers of the same type
    if logger.handlers:
        return logger

    # Set log level to loglevel or to INFO if the requested level is incorrect
    loglevel = getattr(logging, loglevel.upper(), logging.INFO)
    logger.setLevel(loglevel)

    # Define the log message format and date format
    fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
    fmt_date = '%d-%m-%YT%T%Z'
    formatter = logging.Formatter(fmt, fmt_date)

    # Create a file handler to log all messages
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a stream handler to log only warning, error, and critical messages to console
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Log the script running information if logger name is 'root'
    if logger.name == 'root':
        logger.info('Running: %s %s',
                    os.path.basename(sys.argv[0]),
                    ' '.join(sys.argv[1:]))

    return logger


# Create the logger
log = getLogger('root')
import logging
import logging.config


def init_logging(file_path: str,
                 level: str = "DEBUG",
                 maxbytes: int = 1024 * 1024,
                 backup_count: int = 10) -> None:
    """
    Init logging in project
    Possibility to log to file and to console out

    Args:
        file_path (str): path to file that logs will be saved to.
        maxbytes (int, optional): Maximum size of file . Defaults to 1024*1024 which is 10mb.
        backup_count (int, optional): how many backup files to keep. Defaults to 10.

    Returns:
        None.

    """

    config: dict = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {'default': {'()': 'uvicorn.logging.DefaultFormatter', 'fmt': '%(levelprefix)s %(message)s', 'use_colors': None},
                       'access': {'()': 'uvicorn.logging.AccessFormatter', 'fmt': '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'},
                       'file': {'class': 'logging.Formatter', 'format': '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',},},
        'handlers': {'default': {'formatter': 'default', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stderr'},
                     'access': {'formatter': 'access', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout'},
                     'file': {'class': 'logging.handlers.RotatingFileHandler', 'formatter': 'file', 'filename': file_path, 'maxBytes': maxbytes, 'backupCount': backup_count}},
        'loggers': {'uvicorn': {'handlers': ['default'], 'level': 'INFO'},
                    'uvicorn.error': {'level': 'INFO', 'handlers': ['default'], 'propagate': False},
                    'uvicorn.access': {'handlers': ['access'], 'level': 'INFO', 'propagate': False},
                    },
        'root': {
            'level': level,
            'handlers': ['file', "default"],
        }
    }

    logging.config.dictConfig(config)

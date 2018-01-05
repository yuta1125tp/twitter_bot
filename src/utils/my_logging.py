#coding:utf-8
import os

from logging import StreamHandler, DEBUG, INFO, Formatter, FileHandler, getLogger

def my_get_logger(name, log_file_name=None, log_dir='log'):
    """get logger"""
    logger = getLogger(name)

    log_fmt = Formatter('%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)a] %(message)s')
    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(log_fmt)
    logger.addHandler(handler)

    if log_file_name is not None:
        os.makedirs(log_dir, exist_ok=True)
        handler = FileHandler(os.path.join(log_dir, log_file_name), 'a')
        handler.setLevel(DEBUG)
        handler.setFormatter(log_fmt)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
    return logger

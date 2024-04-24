import yaml
import logging


def load_config():
    with open('config.yaml') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise Exception(f'Error loading config: {e}')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

# Path: opencrm/utils/loggers.py

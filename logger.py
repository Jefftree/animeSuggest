import logging

FORMAT = '%(asctime)-15s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.info('Logger initialized')

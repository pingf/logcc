

import logging
import sys
from logging import StreamHandler


class MyHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        self.note = "dameng"
    def emit(self, record):
        record.name = record.name + ' - '+ self.note 
        super().emit(record)

if __name__ == "__main__":
    logger = logging.getLogger("hello.world") 
    logger.setLevel(logging.DEBUG)
    handler = MyHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

    # logging.debug('debug message')
    # logging.info('info message')
    # logging.warning('warning message')
    # logging.error('error message')
    # logging.critical('critical message')



    # # logging.critical('-'*80)
    # # import logging

    # # logging.basicConfig()
    # # logger = logging.getLogger(__name__)
    # # logger.setLevel(logging.DEBUG)


import logging
from multiprocessing import Pool
import os
import test

logger = logging.getLogger(__name__) 


def test(value):
    msg = '{},{}'.format(os.getpid(), value)
    logger.info(msg)
if __name__ == '__main__':
    import logging.config
    import yaml

    path = 'logging.yml'
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
            # print(config)
        logging.config.dictConfig(config)

    test('begin')

    p = Pool(4)
    p.map(test, [1, 2, 3, 4])

    test('end')
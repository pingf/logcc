import logging
import multiprocessing
import os
import sys
import threading
import time
import traceback
from multiprocessing import Pool, Queue
from queue import Empty

from logging.handlers import RotatingFileHandler


class QueueProxy:
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.get('mode', 'multi')
        self.queues = [Queue(-1)] if self.mode == 'single' else [Queue(-1)]*2
    def enqueue(self, data):
        if self.mode == 'single':
            return self.queues[0].put_nowait(data)

        for queue in self.queues:
            if not queue.full():
                queue.put_nowait(data)
                return
        new_queue = Queue(-1)
        new_queue.put(data)
        self.queues.append(new_queue)

    def dequeue(self):
        if self.mode == 'single':
            return self.queues[0].get()
        while True:
            for queue in self.queues:
                if not queue.empty():
                    return queue.get()
            time.sleep(0.01)


class ParallelRotatingHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.queue = QueueProxy(maxsize=kwargs.get('maxsize', -1), mode='single')
        self.thread = threading.Thread(target=self.receive)
        self.thread.setDaemon(kwargs.get('daemon', True))
        if kwargs.get('start', True):
            self.thread.start()


    def receive(self):
        while True:
            try:
                record = self.queue.dequeue()   #self.queue.get_nowait(block=False)
                # record = self.queue.get()
                if record:
                    record.pid = '{}'.format(os.getpid())
                    super().emit(record)
                # time.sleep(100)
            except Exception as e:
                print(e, '????', type(e))
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except Exception as e:
                traceback.print_exc(file=sys.stderr)
            # try:
            #     record = self.queue.get(block=False)
            #     print(record, '.....')
            #     # record.pid = '{}'.format(os.getpid())
            #     # super().emit(record)
            #     # print('received on pid {}'.format(os.getpid()))
            # except (KeyboardInterrupt, SystemExit):
            #     raise
            # except EOFError:
            #     break
            # except Exception as e:
            #     traceback.print_exc(file=sys.stderr)


    def send(self, s):
        try:
            # self.queue.put_nowait(s)
            self.queue.enqueue(s)

        except Exception as e:
            print('timeout')
            print(e, type(e))
            print('.'*100)
            

    def emit(self, record):
        try:
            formatted_record = record#self._format_record(record)
            self.send(formatted_record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def _format_record(self, record):
        # ensure that exc_info and args have been stringified. Removes any
        # chance of unpickleable things inside and possibly reduces message size
        # sent over the pipe
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None
        return record

def job(num):
    logger = logging.getLogger("hello.world") 
    logger.setLevel(logging.DEBUG)
    handler = ParallelRotatingHandler(filename='test.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pid)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for i in range(100000):
        logger.debug('debug message'+str(i))
        print('>', i)
        # time.sleep(1)
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.error('error message')
    # logger.critical('critical message')
    print(num, '-'*100)
    time.sleep(20)

if __name__ == "__main__":
    pool = Pool()
    res = pool.map(job, range(2))
    print(res)


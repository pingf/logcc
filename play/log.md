# python的log入门

## 一个简单的log

```python
import logging
import sys

if __name__ == "__main__":
    # logging.basicConfig()
    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    # handler = logging.FileHandler('output.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
```
上面的代码输出的结果是
```python
2018-11-10 21:55:59,327 - __main__ - INFO - info message
2018-11-10 21:55:59,327 - __main__ - WARNING - warning message
2018-11-10 21:55:59,328 - __main__ - ERROR - error message
2018-11-10 21:55:59,328 - __main__ - CRITICAL - critical message
```
注意上面的代码在输出时千万不要使用logging.info(xxx)这样，因为这样也是会输出的，但是使用的输出等级和预想的可能不一致。


另外， 这里面要熟悉下面几个概念
- logger     日志控制器
- handler    日志处理器
- formater   格式控制器
- filter(上面代码未出现)   日志过滤器


## 使用过滤器
```python
import logging
import sys


if __name__ == "__main__":
    logger1 = logging.getLogger("hello.world") 
    logger2 = logging.getLogger("你好.世界") 
    logger1.setLevel(logging.DEBUG)
    logger2.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    filter_ = logging.Filter("你好")
    handler.addFilter(filter_)

    logger1.addHandler(handler)
    logger2.addHandler(handler)

    logger1.debug('debug message')
    logger1.info('info message')
    logger1.warning('warning message')
    logger1.error('error message')
    logger1.critical('critical message')

    logger2.debug('debug message')
    logger2.info('info message')
    logger2.warning('warning message')
    logger2.error('error message')
    logger2.critical('critical message')
```
filter使用来过滤日志输出的，默认情况下是过滤日志名称（record）的，这里面有两个，分别是"hello.world"和"你好.世界"，而在filter中设置了"你好"，则会过滤"你好*"的日志，输出如下。
```
2018-11-10 22:27:47,820 - 你好.世界 - DEBUG - debug message
2018-11-10 22:27:47,820 - 你好.世界 - INFO - info message
2018-11-10 22:27:47,821 - 你好.世界 - WARNING - warning message
2018-11-10 22:27:47,821 - 你好.世界 - ERROR - error message
2018-11-10 22:27:47,821 - 你好.世界 - CRITICAL - critical message
```

## hack一下过滤器filter, 让其过滤别的东西
```python
import logging
import sys

if __name__ == "__main__":
    logger = logging.getLogger("hello.world") 
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.addFilter(type('', (logging.Filter,), {'filter': staticmethod(lambda r: r.levelno <= logging.INFO)}))
    logger.addHandler(handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
```
这里面通过type构建了一个filter, 这个方式比较hack，当然我们也可以使用继承的方式重写filter方法，这个方法会接收一个record参数。record是一个记录用的对象，日志的名称(name),等级(levelno)等可以在record对象中获得。这段代码使用lambda函数简化了这个重载的方法，使其输出等级低于等于INFO的日志（一般用setLevel设置的只会输出等级更高的），所以输出是
```python
2018-11-10 22:36:35,562 - hello.world - DEBUG - debug message
2018-11-10 22:36:35,562 - hello.world - INFO - info message
```

## 创建一个定制化的handler
```python
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
```
定制logger只需实现一个继承自logger的类，并重写最核心的emit方法即可，注意emit接收的参数是record对象，这里对其的操作是通过record来实现的。上面的程序输出是
```
2018-11-10 22:58:08,859 - hello.world - dameng - DEBUG - debug message
2018-11-10 22:58:08,859 - hello.world - dameng - INFO - info message
2018-11-10 22:58:08,859 - hello.world - dameng - WARNING - warning message
2018-11-10 22:58:08,859 - hello.world - dameng - ERROR - error message
2018-11-10 22:58:08,859 - hello.world - dameng - CRITICAL - critical message
```


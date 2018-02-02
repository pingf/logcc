from logbook import warn, StreamHandler
import sys

from termcc.cc import cc

my_handler = StreamHandler(sys.stdout)
my_handler.push_application()
warn(cc(':red: :yin_yang: This is a warning :reset:'))

import os
from logbook import Processor


def inject_cwd(record):
    record.extra['cwd'] = os.getcwd()


with my_handler.applicationbound():
    with Processor(inject_cwd).applicationbound():
        warn(cc(':blue: :yin_yang: This is a warning'))

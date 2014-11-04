import threading
import sys

stream = sys.stdout

def info(*args):
    stream.write('[{}]: '.format(threading.current_thread().name))
    for i in args:
        stream.write(str(i))
        stream.write(' ')
    stream.write('\n')

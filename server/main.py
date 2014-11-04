#!/usr/bin/python
import config
from threading import Event

def run():
    print('Starting Corpora...')

    app = Event()
    def alive():
        return not app.is_set()

    for name in config.SERVICES:
        service = __import__(name).service
        service.alive = alive
        service.start()
        service.join()

if __name__ == '__main__':
    run()

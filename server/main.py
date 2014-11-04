#!/usr/bin/python
import config
import threading
import trace
import sys

def run():
    threading.current_thread().name = 'main'
    trace.info('Starting Corpora.')

    app = threading.Event()
    def alive():
        return not app.is_set()

    for name in config.SERVICES:
        service = __import__(name).service
        service.alive = alive
        service.start()

    try:
        # Block until any key pressed
        sys.stdin.read()
    finally:
        trace.info('Shutting down.')
        app.set()

if __name__ == '__main__':
    run()

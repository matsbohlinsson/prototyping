#!/usr/bin/env python
import logging
import sys
from io import StringIO


class MyApp():
    def __init__(self):
        self.func_map = {}

    def register(self, name):
        def func_wrapper(func):
            self.func_map[name] = func
            return func
        return func_wrapper

    def call_registered(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("No function registered against - " + str(name))
        return func()

app = MyApp()

@app.register('/')
def main_page_func():
    return "This is the main page."

@app.register('/next_page')
def next_page_func():
    return "This is the next page."

print(app.call_registered('/'))
print(app.call_registered('/next_page'))


logging.basicConfig(filename='v6/logs/logger.log',level=logging.INFO,
                    format = '%(asctime)s,%(msecs)d %(levelname)-8s  %(message)s [%(funcName)s() %(filename)s:%(lineno)d]',
                    datefmt = '%Y-%m-%d:%H:%M:%S',
                    force=True)
log = logging.getLogger(__name__)
handler = logging.StreamHandler(buffer := StringIO())
handler.setFormatter(logging.Formatter('%(lineno)s %(message)s'))
log.addHandler(handler)

log.info("hejhopp")
log.info("hejhopp")
print("qq", buffer.getvalue())
print("")
log.info("hej")
log.info("hej")
print("qq", "".join(buffer.getvalue()))


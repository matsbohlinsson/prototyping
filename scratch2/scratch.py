#!/usr/bin/env python

import sys

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




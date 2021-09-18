#!/usr/bin/env python

import sys

class MyApp():
    def __init__(self):
        self.func = None

    def register(self):
        def func_wrapper(func):
            self.func = func
            return func
        return func_wrapper

    def call_registered(self):
        func = self.func
        return func()

app = MyApp()

@app.register()
def foo():
    print("Foo called")


app.call_registered()




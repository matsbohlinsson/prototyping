import inspect


def myfunc(x:int):
    print("f")
    return 12

my_lambda = lambda x:print("HEJ")

decompiled = inspect.getsource(my_lambda)
print("Q", decompiled)
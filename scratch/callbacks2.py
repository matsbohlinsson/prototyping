

class P():
    pass

class A(P):
    pass

class B:
    pass

a=A()
b=B()

print( isinstance(a, P) )
print( isinstance(b, P) )



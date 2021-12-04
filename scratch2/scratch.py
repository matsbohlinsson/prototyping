

class A:
    def __init__(self):
        self.a=1
        self.qa=1

aa=A()
print([x for x in aa.__dict__])

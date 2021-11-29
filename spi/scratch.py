

PAGE_SIZE=256
def get_pages_from_file(file_name:str):
    pages=[]
    with open(file_name, 'rb') as f:
        while (chunk := f.read(PAGE_SIZE)) != b'':
            pages.append(list(chunk))
    last_page = pages[-1]
    for i in range(PAGE_SIZE - len(last_page)):
        last_page.append(255)
    return pages

b=get_pages_from_file('spi_flash.py')
for i in b:
    print(len(i), i)




class Input:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = "qww"

class A():
    def __init__(self):
        self.input = Input()
        self.a = 1

    def foo(self):
        print(self.input.d)
        pass


q=A()
a = q.input.d
q.input.my_var=10

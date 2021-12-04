import mmap

class MemoryMappedFile():
    def __init__(self, filename:str, page_size:int =256):
        fh = open(filename, mode="r", encoding="utf8")
        self.file_buf = mmap.mmap(fh.fileno(), length=0, access=mmap.ACCESS_READ)
        self.page_size=page_size

    def get_page(self, page_number:int=0):
        pos:int = page_number*self.page_size
        return self.file_buf[pos:pos+self.page_size]


buf = MemoryMappedFile("C:\\Users\\MatsB\\Downloads\\DaVinci_Resolve_Studio_17.4.2_Windows.zip")


print(buf.get_page(30000)[2])



b1 = b'\x01\x02\x03'
b_int_array = [1,2,3]

b_bytes = bytearray([1,2,3])
if b1==b_bytes:
    print("hejhopp")

print(len(buf.file_buf))



print("HEJ")

a=0
a+=1
a+=2

print(a)
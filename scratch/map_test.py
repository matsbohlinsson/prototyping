#!/usr/bin/python3
import functools
import os
import mmap
import time
from pathlib import Path


def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure

@timefunc
def memory_map(filename, access=mmap.ACCESS_READ):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)



@timefunc
def get_pages_from_file(file_name:Path, page_size:int=256, pad_last_page=0xff) -> [[int]]:
    pages=[]
    print("Reading flashfile")
    with open(file_name.absolute(), 'rb') as f:
        while (chunk := f.read(page_size)) != b'':
            pages.append(list(chunk))
    # Fill last page to PAGE_SIZE
    last_page = pages[-1]
    for i in range(page_size - len(last_page)):
        last_page.append(pad_last_page)
    print("Done reading flashfile")
    return pages

@timefunc
def read_last_page(mapped_file):
    return mapped_file[256:512][0]

@timefunc
def make_pages(mapped_file):
    l = []
    size = len(mapped_file)
    for i in range(0, int(size/256-10)):
        l.append([mapped_file[i*256:(i+1)*256]])
    return l


FILE_DEFAULT = '/home/root/firmware/binary/vp-fpga/vp-fpga_mux_spi_ti_flash.bin'
map1 = memory_map(FILE_DEFAULT)

print("mapped", read_last_page(map1))

ll = make_pages(map1)
print("ll", ll[10])

map2 = get_pages_from_file(Path(FILE_DEFAULT))

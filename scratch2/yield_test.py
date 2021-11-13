import time
def download_page():
    yield 'sleep', 1
    print("After 1st yield")
    for i in range(10):
        print("Running in download_page")
        time.sleep(0.2)
    yield 'sleep', 1
    time.sleep(2)
    yield 'sleep', 1
    time.sleep(2)
    return '<html>body</html>'

def download_page2():
    yield 'sleep', 1
    print("2After 1st yield")
    for i in range(10):
        print("2Running in download_page")
        time.sleep(0.2)
    yield 'sleep', 1
    time.sleep(2)
    yield 'sleep', 1
    time.sleep(2)
    return '<html>body</html>'

def printtime(i: int):
    print(f'{i}: {time.time():.2f}')

start = time.time()
printtime(0)
page_downloader = download_page()
page_downloader2 = download_page2()
printtime(1)
page_downloader.send(None)
page_downloader2.send(None)
page_downloader.send(None)
page_downloader2.send(None)
for i in range(10):
    print("Running in main")
    time.sleep(0.2)
printtime(2)
page_downloader.send(None)
printtime(3)
page_downloader.send(None)
printtime(4)

print(f'time used:{time.time() -start}')

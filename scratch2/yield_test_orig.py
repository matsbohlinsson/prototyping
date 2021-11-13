import time
def download_page():
    print('start connecting web server...')
    yield 'sleep',1
    time.sleep(1)
    print('start download page')
    yield 'sleep',1.5
    time.sleep(1.5)
    print('finish web downloading')
    return '<html>body</html>'

def read_db():
    print('start connecting db server...')
    yield 'sleep',0.5
    time.sleep(0.5)
    print('start db reading...')
    yield 'sleep',1.5
    time.sleep(1.5)
    print('finish db reading')
    return '{data:json_data}'

start = time.time()
page_downloader = download_page()
db_reader = read_db()
page_downloader.send(None)
db_reader.send(None)
page_downloader.send(None)
db_reader.send(None)
print(f'time used:{time.time() -start}')
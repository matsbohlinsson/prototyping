import asyncio
from asyncio import sleep 
#import nest_asyncio     # uncomment it in Juptyer Notebook
#nest_asyncio.apply()    # uncomment it in Juptyer Notebook

import time
from queue import Queue
import heapq

async def download_page():
    print('start connecting web server...')
    await sleep(1)
    print('start download page')
    await sleep(1.5)
    print('finish web downloading')
    return '<html>body</html>'

async def write_db(data):
    print('start connecting db server...')
    await sleep(0.5)
    print('start db writing...')
    await sleep(1.5)
    print('finish db writing')

async def main():
    page = await download_page()
    await write_db(page)

start = time.time()
asyncio.run(
    asyncio.gather(main(),main(),main(),main())
)
end = time.time()
print(f'used time {end - start}')
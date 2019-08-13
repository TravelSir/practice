import asyncio
import time


async def add(x=1, y=2):
    print(f'Add {x} + {y}')
    await asyncio.sleep(2)
    return x+y


s = time.time()
loop = asyncio.get_event_loop()
tasks = [add(x, y) for x, y in zip(range(1, 10), range(11, 20))]
# loop.run_until_complete(asyncio.wait(tasks))
# 因为run_until_complete只接受单个future，所以用gather将多个future聚合成一个future
loop.run_until_complete(asyncio.gather(*tasks))

# 结果是未阻塞的运行了2s
print(f'cost {time.time()-s}')

loop.close()



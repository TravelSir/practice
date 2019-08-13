import asyncio
import random


async def add(x=1, y=2):
    print(f'Add {x} + {y}')
    await asyncio.sleep(2)
    return x + y


async def add2(x=1, y=2):
    await asyncio.sleep(random.uniform(1, 5))
    return x+y

loop = asyncio.get_event_loop()

# gather
# gather的顺序是添加到gather时的顺序
# group3 = asyncio.gather(*[add(x, y) for x, y in zip(range(7, 10), range(16, 19))])
# group2 = asyncio.gather(*[add(x, y) for x, y in zip(range(4, 7), range(13, 16))])
# group1 = asyncio.gather(*[add(x, y) for x, y in zip(range(1, 4), range(10, 13))])
#
# # 可以单独取消一组任务
# group2.cancel()
#
# # 因为gather已经将future丢到loop中了，所以这里执行一次空future就把之前到future一起执行了
# loop.run_until_complete(asyncio.gather())


# wait
tasks = [add2(x, y) for x, y in zip(range(1, 10), range(11, 20))]
# wait可以在完成第一个future完成或超时后等待停止
finished, unfinished = loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
print('get first result:')
for task in finished:
    print(task.result())

print(f'unfinished:{len(unfinished)}')

print('get more result in 2 seconds:')
finished2, unfinished2 = loop.run_until_complete(
    asyncio.wait(unfinished, timeout=2))
for task in finished2:
    print(task.result())
print(f"unfinished2:{len(unfinished2)}")

print("Get all other results:")
finished3, unfinished3 = loop.run_until_complete(asyncio.wait(unfinished2))
for task in finished3:
    print(task.result())

loop.close()

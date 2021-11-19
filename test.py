from libs.uasyncio.queues import Queue
from libs import uasyncio as asyncio
q = Queue()


async def producer(q):
    while True:
        await q.put(42)  # may pause if a size limited queue fills
        print('afer sleep')
        await asyncio.sleep(2)
        


async def consumer(q):
    while True:
        result = await(q.get())  # Will pause if q is empty
        print('Result was {}'.format(result))



loop = asyncio.get_event_loop()
loop.create_task(consumer(q))
loop.create_task(producer(q))





loop.run_forever()


import pyb
from libs import uasyncio as asyncio
import gc

class LEDScheduler():
    def __init__(self, led_num, duration=500):
        self.led = pyb.LED(led_num)
        self.duration = duration
        loop = asyncio.get_event_loop()
        loop.create_task(self._run())
        # loop.run_forever()

    async def _run(self):
        while True:
            await asyncio.sleep_ms(self.duration)
            self.led.toggle()
            gc.collect()
            gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
            

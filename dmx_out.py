import utime
import pyb
from array import array
from libs import uasyncio as asyncio
from libs.uasyncio.queues import Queue

from pyb import udelay

class DMXWriter():
    def __init__(self, dmx512_out_serial=None, dmx512_queue=None):
        self.dmx512_out_serial = dmx512_out_serial
        self.dmx512_queue = dmx512_queue
        self.dmx512_enable_output = pyb.Pin('X1', pyb.Pin.OUT_PP) #  ПОДКЛЮЧИТЬ К 5 ВОЛЬТАМ"???
        self.dmx512_enable_output.high() #  x11 enable transmit-1,enable receive-0
        
        # self.dmx512_send_break = pyb.Pin('X3', Pin.OUT_OD)
        
        # https://docs.python.org/3/library/array.html
        self.dmx512_buffer = array('B', [0] * 5)
        self.swriter = asyncio.StreamWriter(dmx512_out_serial, {})
        
        loop = asyncio.get_event_loop()
        loop.create_task(self._run())
    
    async def _run(self):
        while True:
            # # for ch in message:
            #     # self.dmx_message[ch] = message[ch]
            # dmx1.set_channels({1:10, 2:5, 3:30})
        # for i, ch in enumerate(channels):
        #     self.dmx_message[ch] = values[i]
            
            frame = await self.dmx512_queue.get()
            # print('got frame', frame)
            self.dmx512_out_serial.sendbreak()
            await self.swriter.awrite(frame)
            await asyncio.sleep_ms(0)
 



from libs import uasyncio as asyncio
from pyb import udelay
from array import array
import random
import color_spaces
import limiter
from midi_message import MidiMessage
from libs.uasyncio.queues import Queue
from libs.uasyncio.asyn import NamedTask
from libs.uasyncio.asyn import cancellable
from color_spaces import HSV
import utime


class Fader():
    def __init__(self, dmx512_queue=None, midi_messages_queue=None):
        self.dmx512_queue = dmx512_queue
        self.midi_messages_queue = midi_messages_queue
        self.dmx512_buffer = array('B', [0] * 5)
        self.hsv = HSV()
        ''''''
        self._attacking = False
        self._releasing = False


        ''''''
        loop = asyncio.get_event_loop()
        loop.create_task(self._run())

        self.attack_length = .8    
        self.release_length = .8   

    # attack_length = limiter.Limiter(min=0.007874015748031496, max=1.0)
    # release_length = limiter.Limiter(min=0.007874015748031496, max=1.0)
    
    async def _run(self):
        while True:
            # print(self.midi_messages_queue.qsize())
            # if self.midi_messages_queue.empty():
            #message = await self.midi_messages_queue.get()


            # await NamedTask('attack', self.attack)
            # await NamedTask('release', self.release)

            # if self._attacking:
            #     await NamedTask.cancel('attack', nowait=False)
            # if self._releasing:
            #     await NamedTask.cancel('release', nowait=False)

            await self.dmx512_queue.put(self.dmx512_buffer)
            # print('queue put->', dmx512_buffer)
            await asyncio.sleep_ms(1)
    
    @cancellable
    async def attack(self):
        # print('attack')
        # self._releasing = False
        # self._attacking = True
        # await asyncio.sleep_ms(0)

        self._radnomize_color()

        self.hsv.Value = 0
    

        V = 1.0 / self.attack_length  # V=S/t
        remain_S = 1.0 - self.hsv.Value

        remain_t = remain_S / V
        remain_t = remain_t * 1000

        end_time = utime.ticks_add(utime.ticks_ms(), int(remain_t))
        print('before: ', utime.ticks_ms(), end_time)
        
        while utime.ticks_ms() < end_time:
            # if self._releasing:
            #     await NamedTask.cancel('attack', nowait=False)
            #     await asyncio.sleep_ms(0)
            t_remained = end_time -  utime.ticks_ms()  # осталось
            # print('T_REMAINED: ', t_remained)
            h = round((1000 - t_remained * V)/1000, 3)
            # print('Hue: ',  h)
            self.hsv.Value = round((1000 - t_remained * V)/1000, 3)
            self._switch_color()
            await asyncio.sleep_ms(0)
        self.hsv.Value = 1.0
        self._switch_color()
        # await asyncio.sleep_ms(0)

    @cancellable
    async def release(self):
        # print('release')
        # self._attacking = False
        # self._releasing = True
        # await asyncio.sleep_ms(0)

        V = 1.0 / self.release_length
        remain_S = self.hsv.Value
        remain_t = remain_S / V

        remain_t = remain_t * 1000
        
        end_time = utime.ticks_add(utime.ticks_ms(), int(remain_t))
        # end_time = time.time() + remain_t
        while utime.ticks_ms() < end_time:
            # if self._attacking:
            #     await NamedTask.cancel('release', nowait=False)
            #     await asyncio.sleep_ms(0)
            t_remained = end_time - utime.ticks_ms()  # осталось
            self.hsv.Value = ( t_remained * V)/1000
            self._switch_color()
            await asyncio.sleep_ms(0)
            # print('releasing:', self.hsv.Value)
        self.hsv.Value = 0  # нужно для больших скоростей
        self._switch_color()
        # await asyncio.sleep_ms(0)








    def _switch_color(self):
        data = self.hsv.toRGB()
        self.dmx512_buffer[1] = data.R
        self.dmx512_buffer[2] = data.G
        self.dmx512_buffer[3] = data.B
        

    def set_attack_length(self, cc_value):
        self.attack_length = cc_value / 127

    def set_release_length(self, cc_value):
        self.release_length = cc_value / 127

    def _radnomize_color(self):
        randomHue = round(random.random(), 3)
        self.hsv.Hue = randomHue



        
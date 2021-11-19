# main.py -- put your code here!
'''DOX
https://github.com/peterhinch/micropython-async/blob/master/FASTPOLL.md
https://github.com/peterhinch/micropython-async
https://github.com/peterhinch/micropython-async/blob/master/FASTPOLL.md
'''
import pyb
from libs.uasyncio.queues import Queue

from ssd1306 import SSD1306
display = SSD1306(pinout={'sda': 'Y10', 'scl': 'Y9'}, height=64, external_vcc=False)

try:
    display.poweron()
    display.init_display()
    x = 0
    y = 0
    direction_x = True
    direction_y = True
    display.draw_text(10,10,'test',size=1,space=1)
    display.display()

except Exception as ex:
    led_red.on()
    print('Unexpected error: {0}'.format(ex))
    display.poweroff()


# print((msg_bytes[0]))
#self.lcd.draw_text(10,10,s,size=1,space=1)
#display.display()


from led_scheduler import LEDScheduler
from midi_in import MidiInput
from dmx_out import DMXWriter
from fader import Fader
from midi_parser import MidiParser

# import gc
# gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
# http://docs.micropython.org/en/latest/reference/constrained.html


async def rr(n):
    while True:
        print('Roundrobin ', n)
        await asyncio.sleep(0)


'''
My approach is to import necessary modules, perform a GC, then allocate any required large buffers. Then run the rest of the application.
'''

from libs import uasyncio as asyncio
loop = asyncio.get_event_loop()

# init queues
midi_messages_queue = Queue()
dmx512_queue = Queue()


#init fader
fader = Fader(dmx512_queue=dmx512_queue, midi_messages_queue=midi_messages_queue)
#init parser
parser = MidiParser(fader=fader, midi_messages_queue=midi_messages_queue)
# init midi input
midi_in_serial = pyb.UART(1, 31250, parity=None, stop=1)
midi_input = MidiInput(midi_in_serial=midi_in_serial, midi_messages_queue=midi_messages_queue, debug=False)

# init dmx512 output
dmx512_out_serial = pyb.UART(2, 250000, bits=8, parity=None, stop=2)
dmx512_out = DMXWriter(dmx512_out_serial=dmx512_out_serial, dmx512_queue=dmx512_queue)

# start led scheduler
led_scheduler = LEDScheduler(3)


# async def producer():
#     i=0
#     while True:
#         i+=1
#     if i > 254:
#         i=0
#     print('produced')
#     dmx512_queue.put(i)

# loop.create_task(producer())



loop.run_forever()

                    # if on==' note_on ':
                    #     dmx1.set_channels({1:90, 2:5, 3:160})
                    # else:
                    #     dmx1.set_channels({1:0, 2:0, 3:0})
                    # dmx1.write_frame()
                    # display.draw_text(10,30,on,size=1,space=1)
                    # display.display()







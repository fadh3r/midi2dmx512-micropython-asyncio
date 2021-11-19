from midi_message import MidiMessage
from libs import uasyncio as asyncio
from midi_message import MidiMessage
from libs.uasyncio.queues import Queue
from libs.uasyncio.asyn import NamedTask
from libs.uasyncio.asyn import cancellable

class MidiParser():
    def __init__(self, fader=None, midi_messages_queue=None):
        self.fader = fader
        self.midi_messages_queue = midi_messages_queue
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._run())
        
        


    async def _run(self):
        while True:
            self._message = await self.midi_messages_queue.get()
            # print('queue size: ', self.midi_messages_queue.qsize())
            await self._process_message()
            await asyncio.sleep(0)

    def _process_message(self):
        # await NamedTask('release', self.fader.release)
        # await NamedTask('attack', self.fader.attack)
        
        if self._message.type == 'note_on':
            await NamedTask.cancel('release', nowait=False)
            # print('note_on')
            self.loop.create_task(NamedTask('attack', self.fader.attack)())

        elif self._message.type == 'note_off':
            await NamedTask.cancel('attack', nowait=False)
            # print('note_off')
            self.loop.create_task(NamedTask('release', self.fader.release)())

        # elif self._message.type == 'control_change':
        #     if self._message.control == 13:
        #         self.fader.set_attack_length(self._message.value)
        #     elif self._message.control == 14:
        #         self.fader.set_release_length(self.message.value)   
            



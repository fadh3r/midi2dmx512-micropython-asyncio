'''DOX
https://github.com/SpotlightKid/micropython-stm-lib/blob/master/midi/midi/midiin.py
https://learn.sparkfun.com/tutorials/midi-tutorial/all
https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md
'''
import pyb
from libs import uasyncio as asyncio
from midi_message import MidiMessage
from libs.uasyncio.queues import Queue


class MidiInput:
    def __init__(self, midi_in_serial=None, midi_messages_queue=None, debug=False):
        self.midi_in_serial = midi_in_serial
        self.midi_messages_queue = midi_messages_queue
        self.debug = debug
        self._msgbuf = None
        self._status = None
        self.sreader = asyncio.StreamReader(self.midi_in_serial)
        loop = asyncio.get_event_loop()
        loop.create_task(self._run())
        # loop.run_forever()

    def _error(self, msg, *args):
        if self.debug:
            import sys
            print(msg % args, file=sys.stderr)
    
    async def _run(self):
        while True:
            data = await self.sreader.readexactly(1)
            await self._construct_midi_message(data)
            await asyncio.sleep(0)
 
    def _construct_midi_message(self, data):
        if int.from_bytes(data, 0) & 0x80:  # if status byte
        # (NoteOff 0x8_, NoteOn 0x9_, ControlChange 0xB_)
        # print('status: ', hex(data))
            self._status = data
            self._msgbuf = bytearray(data)

        else:  # if data byte
            if self._status and not self._msgbuf:  # Running status assumed
                '''after first status byte of CC message, there are no more CC status bytes in flow?,
                only if you change MIDI message back and forth'''
                self._msgbuf = bytearray(self._status)

            if not self._status:
                # self._msgbuf = None
                self._error("self._status is empty, data is: 0x%0X." % data)

            if not self._msgbuf:
                # self._status = None
                self._error("Read unexpected data byte 0x%0X." % data)

            self._msgbuf.extend(data)

            if len(self._msgbuf) == 3:
                await self._process_midi_message()
                # msg = MidiMessage(self._msgbuf)
                # await self.midi_messages_queue.put(msg)
                # print('q size:', self.midi_messages_queue.qsize ())
                
                self._msgbuf = None

    def _process_midi_message(self):
        if self._msgbuf:
            midi_message = MidiMessage(self._msgbuf)
            await self.midi_messages_queue.put(midi_message)
        if self.debug:
            pyb.LED(4).toggle()
            self._debug(self._msgbuf)

    def _debug(self, msg_bytes):
        # print(msg_bytes)
        # s = " ".join("%02X " % b for b in msg_bytes) + "  " * (3 - len(msg_bytes))
        # print(s)
        m = MidiMessage(msg_bytes)
        print('debug message: ', m)


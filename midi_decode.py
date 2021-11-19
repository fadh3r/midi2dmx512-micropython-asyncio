    SPECS = [
    _defmsg(0x80, 'note_off', ('channel', 'note', 'velocity'), 3),
    _defmsg(0x90, 'note_on', ('channel', 'note', 'velocity'), 3),
    _defmsg(0xb0, 'control_change', ('channel', 'control', 'value'), 3),
    ]
'''
    In Python 3 you can pass a byte string::

        >>> list(b'\x01\x02\x03')
        [1, 2, 3]
----------
Each midi message consists of 3 bytes.
The first byte is the sum of the command and the midi channel (1-16 > 0-F).
the value of bytes 2 and 3 (data 1 and 2) are dependant on the command.
command+ch     data1                   data2                  Description
----------     -----                   -----                  -----------
0x80-0x8F   Key # (0-127)           Off Velocity (0-127)   Note Off
0x90-0x90   Key # (0-127)           On Velocity (0-127)    Note On
0xB0-0xB0   Control # (0-127)       Control Value (0-127)  Control
http://www.midi.org/techspecs/midimessages.php
-----
A midi message sends data as 7 bit values between 0 and 127.
    if 0 <= value < 2 ** 7:

'''

class MidiMessage():
    def __init__(self, msg_bytes):
        self._msg_status_byte = msg_bytes[0]
        self._msg_data = msg_bytes[1:]
        self.channel = None
        self.note = None
        self.velocity = None
        self.control_change = None
        




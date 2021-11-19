
class MidiMessage:
    def __init__(self, msg_bytes):
        self._msg_status_byte = msg_bytes[0]
        self._msg_data = msg_bytes[1:]
        self.type = None
        self.channel = None
        self.note = None
        self.velocity = None
        self.control_change = None
        self.decode_message()
    
    def decode_message(self):
        # <message note_on channel=2 note=60 velocity=64 time=0>
        status = {144:'note_on', 128:'note_off', 176:'control_change'}
        if self._msg_status_byte & 0xf0 in status:
            self.type = status[self._msg_status_byte & 0xf0]
        self.channel = self._msg_status_byte & 0x0f
        self.note = self._msg_data[0]
        self.velocity = self._msg_data[1]
    
    def __repr__(self):
        message = 'ch:' + str(self.channel) +\
                ' msg:' + str(self.type) +\
                ' note:' + str(self.note) +\
                ' velocity:' + str(self.velocity)
        return message
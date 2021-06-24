import rtmidi
from collections import namedtuple

from datetime import datetime, timedelta


Message = namedtuple('Message', ['type', 'note', 'velocity'])
DatedMessage = namedtuple('DatedMessage', ['message', 'delta'])


class Looper:
    def __init__(self):
        self.midiin = rtmidi.MidiIn()
        self.midiout = rtmidi.MidiOut()
        self.loop = []
        self.loop_length = None
        self.midiin.open_port(0)
        self.midiout.open_virtual_port("My virtual output")

    def record(self, seconds: int):
        self.loop = []
        self.loop_length = timedelta(seconds=seconds)
        with self.midiin:
            listen_start = datetime.now()
            while listen_start + self.loop_length > datetime.now():
                raw_message = self.midiin.get_message()
                if raw_message is not None:
                    message = Message(*raw_message[0])
                    delta = datetime.now() - listen_start
                    self.loop.append(DatedMessage(delta=delta, message=message))
        return len(self.loop)

    def play(self, times: int):
        if not self.loop or not self.loop_length:
            return

        with self.midiout:
            for _ in range(times):
                play_start = datetime.now()
                loop_index = 0
                while play_start + self.loop_length > datetime.now():
                    if loop_index >= len(self.loop):
                        continue

                    message = self.loop[loop_index]
                    if datetime.now() > play_start + message.delta:
                        self.midiout.send_message(list(message.message))
                        loop_index += 1

    def close(self):
        self.midiin.close_port()
        self.midiout.close_port()

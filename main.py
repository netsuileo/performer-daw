import time
import copy
import rtmidi
from dataclasses import dataclass
from collections import namedtuple
from datetime import datetime, timedelta

midiout = rtmidi.MidiOut()
midiin = rtmidi.MidiIn()
available_ports = midiout.get_ports()

midiin.open_port(1)
midiout.open_virtual_port("My virtual output")

LOOP_LENGTH = timedelta(seconds=4)
PRESSED = 144
RELEASED = 128

Message = namedtuple('Message', ['type', 'note', 'velocity'])

@dataclass
class DatedMessage:
    message: Message
    delta: timedelta

last_note_pressed = None
last_note_pressed_datetime = None

with midiin:
    with midiout:
        loop = []
        # wait for anything from keyboard
        input()

        listen_start = datetime.now()
        while listen_start + LOOP_LENGTH > datetime.now():
            raw_message = midiin.get_message()
            if raw_message is not None:
                message = Message(*raw_message[0])
                print(message)
                midiout.send_message(list(message))
                delta = datetime.now() - listen_start
                loop.append(DatedMessage(delta=delta, message=message)) 

        print("-------------------------------")
        print("LOOPING!")
        print("-------------------------------")

        while True:
            play_start = datetime.now()
            loop_index = 0
            while play_start + LOOP_LENGTH > datetime.now():
                if loop_index >= len(loop):
                    continue

                message = loop[loop_index]
                if datetime.now() > play_start + message.delta:
                    print(message.message)
                    midiout.send_message(list(message.message))
                    loop_index += 1

            for message in loop:
                if message.message.type == PRESSED:
                    new_message = copy.copy(message)
                    new_message.type = RELEASED
                    midiout.send_message(list(message.message))

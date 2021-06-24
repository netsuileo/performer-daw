import cmd

class DawShell(cmd.Cmd):
    def __init__(self, looper):
        self.looper = looper
        super().__init__()

    def do_record(self, arg: str):
        seconds = int(arg)
        print(f"Recording for {seconds} seconds.")
        messages = self.looper.record(seconds)
        print(f"Recorded {messages} messages.")

    def do_play(self, arg: str):
        times = int(arg)
        if not self.looper.loop:
            print(f"Nothing recorded yet")
            return

        print("Playing!")
        self.looper.play(times)

    def do_quit(self, arg: str):
        self.looper.close()
        return True

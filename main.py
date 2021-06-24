from shell import DawShell
from looper import Looper

def main():
    looper = Looper()
    shell = DawShell(looper)
    shell.cmdloop()

if __name__ == '__main__':
    main()

from queue import Queue, Empty
from keyboard import on_press_key
from pygetwindow import getActiveWindowTitle
from time import sleep
from exceptions import SkipTask


def pauseFunc(t : int):
        while True:
            if 'r' == Command.queue.get():
                Command.checkCommand(t)
                return
class Command:
    commandObjects = [
        {
            "letter" : "p",
            "help" : "pause task progress",
            "func" : pauseFunc 
        },
        {
            "letter" : "r",
            "help" : "resume task progress",
            "func" : lambda t : sleep(t)
        },
        {
            "letter" : "s",
            "help" : "skip task",
            "func" :lambda _ : (_ for _ in ()).throw(SkipTask())
        },
        {
            "letter" : "e",
            "help" : "exit the application",
            "func" : lambda _ : (_ for _ in ()).throw(SystemExit())
        }
    ]
    
    queue = Queue()
    commands  = []
    def __init__(self, letter : str, help : str, func) -> None:
        self.letter = letter
        self.help = help
        self.func = func
        on_press_key(self.letter, lambda _ : self.send())
        Command.commands.append(self)
        
        
    
    def send(self):
        title : str = getActiveWindowTitle()    
        if title.endswith("focus.exe") or "focus.io" in title:
            Command.queue.put(self.letter)
            
    def __str__(self) -> str:
        return f"({self.letter})    {self.help}"
            
    @classmethod
    def initialize_commands(cls):
        for command in cls.commandObjects:
            Command(**command)
            
            
    @classmethod
    def print_help(cls):
        print("Available commands: ")
        for command in cls.commands:
            print(command)
    
    @classmethod
    def checkCommand(cls, sleeping : int):
        try:
            t = Command.queue.get(True, sleeping)
            for command in cls.commands:
                if command.letter == t:
                    command.func(sleeping)
                    return
            sleep(sleeping)
        except Empty :
            pass
        
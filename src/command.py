from queue import Queue
from keyboard import on_press_key
from pygetwindow import getActiveWindowTitle

class Command:
    commands = [
        {"letter" : "p", "help" : "pause task progress"},
        {"letter" : "r", "help" : "resume task progress"},
        {"letter" : "s", "help" : "skip task"},
        {"letter" : "e", "help" : "exit the application"}
    ]
    queue = Queue()
    def __init__(self, letter : str) -> None:
        on_press_key(letter, lambda _ : self.send(letter))
        
    
    def send(self, l : str):
        title : str = getActiveWindowTitle()    
        if title.endswith("focus.exe") or "focus.io" in title:
            Command.queue.put(l)
            
    @classmethod
    def initialize_commands(cls):
        for command in cls.commands:
            Command(command['letter'])
            
    @classmethod
    def print_help(cls):
        print("Available commands: ")
        for command in cls.commands:
            print(f"({command['letter']})    {command['help']}")
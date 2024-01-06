from pyttsx3 import speak
from time import sleep
from traceback import print_exc
from sys import stdout, exit
from json import load
from setup import focus
from shutil import get_terminal_size
from pam import find

__version__ = "01.01.01"

class Task:

    tasks = []

    def __init__(self, name : str, duration : int, msg = None):
        self.name = name
        self.duration = duration
        
        if not msg:
            self.msg = f"Now is {self.name} time, you will have to do it for {self.duration} minutes"
        else: 
            self.msg = msg

        Task.tasks.append(self)

terminal, indent, bar = None, None, None

mins_left: int = None


# ----------------MAIN FUNCTION------------------#
# ----------------MAIN FUNCTION------------------#
def main():
    global mins_left, terminal, indent, bar

    terminal, indent, bar = get_terminal_data()

    print(focus)

    speak("Welcome to FOCUS.io, please enter the things you want to do")

    get_details()

    while True:
        for task in Task.tasks:

            terminal, indent, bar = get_terminal_data()

            side_space = int((terminal - len(task.msg)) / 2)
            print("\n\n")
            print(" " * side_space, task.msg, sep="")
            speak(task.msg)

            progressbar(task.duration * 60 / bar)

        cong = "Congratulations, you had just completed a whole loop!"
        l = int((terminal - len(cong)) / 2)
        print(" " * l, cong, sep="")
        speak(cong)

def get_details():
    count = 1
    while True:
        try:
           task = input(f"{count}: ")
        except:
            exit()
        match task:
            case "R" :
                Task.tasks = []
                count = 1
                continue
            case "":
                if len(Task.tasks) < 1:
                    exit()
                return
            case _:
                count += 1
                pass
        if not saved(task):
            Task(task, get_duration())

        
def progressbar(sleeping):

    print(" " * indent, "_" * bar, sep="")
    print(" " * (indent - 1), "[", sep="", end="")

    for _ in range(bar):
        try:
            sleep(sleeping)
        except KeyboardInterrupt:
            while True:
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    break
            try:
                sleep(sleeping)
            except KeyboardInterrupt:
                try:
                    sleep(0.8)
                    sleeping = 0
                except KeyboardInterrupt:
                    exit()
        stdout.write("=")
        stdout.flush()

    print("]\n", " " * indent, "_" * bar, "\n\n", sep="")
    

def saved(shortcut):
    with open(find("saved.json")) as file:
        saved_data = load(file)
    
    if shortcut in saved_data:
        duration = saved_data[shortcut]['duration']
        print(f"duration is set as defult: {duration}")
    elif shortcut.lower() in saved_data:
        duration = get_duration()
    else:
        return
    
    obj = saved_data[shortcut.lower()]
    Task(obj['name'], duration, obj['msg'])
    return True

def get_duration():
    while True:
        try:
            return int(input("Duration: "))
        except ValueError:
            continue

def get_terminal_data():
    terminal: int = int(
    str(get_terminal_size()).replace("os.terminal_size(columns=", "").split(",")[0]
)
    indent: int = int(terminal / 25)
    bar: int = int((terminal / 25) * 23)
    return terminal, indent, bar

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        exit()
    except BaseException as e:
        print_exc()
        input("Press enter to exit: ")

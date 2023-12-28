from pyttsx3 import speak
from time import sleep
from plyer import notification as nf
from sys import stdout, exit
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from setup import focus
from shutil import get_terminal_size
import csv

__version__ = "00.00.00"

class NoTasksDefined(Exception):
    ...

class Task:

    tasks = []

    def __init__(self, name, msg, duration):
        self.name = name
        self.duration = duration
        
        if msg == 0:
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

    i = 1
    while True:
        x = get_details(Task.tasks, i)
        if x == False:
            break
        elif x == "RESTART":
            Task.tasks = []
            i = 1
            continue
        i += 1

    if i == 1:
        raise NoTasksDefined("You didnt's input any tasks")

    while True:
        for task in Task.tasks:

            terminal, indent, bar = get_terminal_data()

            l = int((terminal - len(task.msg)) / 2)
            print("\n\n")
            print(" " * l, task.msg, sep="")
            speak(task.msg)

            progressbar(task.duration)

        cong = "Congratulations, you had just completed a whole loop!"
        l = int((terminal - len(cong)) / 2)
        print(" " * l, cong, sep="")
        speak(cong)


def get_details(n: int = 1, errormsg: str = "Please enter a valid number"):
    """A function that gets the details of every thing the user gonna do"""
    input_ = input(f"{n}: ")
    if input_ == "":
        return False
    if input_ == "R":
        return "RESTART"
    x = is_saved(list, input_)
    if x == 1:
        print(f"Duration is set as default: {list[n - 1]['time']}")
        return True
    else:
        while True:
            try:
                duration = int(input("Duration: "))
                break
            except ValueError:
                print(errormsg)

    Task(input_, x, duration)
    return True


def progressbar(n):
    """Deals with the animation bar process"""

    # Print the progress bar
    print(" " * indent, "_" * bar, sep="")
    print(" " * (indent - 1), "[", sep="", end="")

    mins_left = n * 60
    for i in range(bar):
        mins_left = minisleep(n, mins_left)
        stdout.write("=")
        stdout.flush()

    print("]\n", " " * indent, "_" * bar, "\n\n", sep="")


def minisleep(n, mins):
    """Wait for the n/bar\n
    Divides the time by the bar and with every bar percent from the time it ends"""

    for _ in range(int((n * 60) / bar * 100)):
        sleep(0.01)
    mins -= mins / bar

    return mins


def is_saved(list, x):
    with open("saved.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if x != row["shortcut"]:
                if x.lower() == row["shortcut"]:
                    return row["intromsg"]

            if x == row["shortcut"]:
                list.append(
                    {
                        "name": row["name"],
                        "msg": row["intromsg"],
                        "time": row["time_default"],
                    }
                )
                file.close()
                return 1

    return 0

def get_terminal_data():
    terminal: int = int(
    str(get_terminal_size()).replace("os.terminal_size(columns=", "").split(",")[0]
)
    indent: int = int(terminal / 25)
    bar: int = int((terminal / 25) * 23)
    return terminal, indent, bar

if __name__ == "__main__":
    main()

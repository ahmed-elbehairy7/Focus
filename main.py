#!/usr/bin/python3

from pyttsx3 import speak
from time import sleep
from traceback import print_exc
from sys import stdout, exit
from json import load, dump
from shutil import get_terminal_size
from os import popen
from inputimeout import inputimeout, TimeoutOccurred

# ----------------MAIN FUNCTION------------------#
# ----------------MAIN FUNCTION------------------#

SAVED_TASKS = r"D:\\pam\\focus.io\\saved.json"
DO = r"D:\\pam\\focus.io\\.do"


def main():
    # Take those global variables to allow editing them for making custom sized progress bar for each task for better visualization
    global terminal, indent, bar

    # Get the size of the terminal, progress bar, and the indentation before printing the progress bar
    terminal, indent, bar = get_terminal_data()

    # print an intro for the application
    # print(focus)

    # Make the computer say the following
    speak("Welcome to FOCUS.io")

    Task.get_tasks("Please enter the one time tasks", True)
    Task.get_tasks("Please enter the looping tasks")

    # Forever:
    while True:
        # For each task added by the user
        for task in Task.tasks:
            task.exec()

        Task.congrats()
        Task.filter_tasks()


class Task:
    tasks = []

    def __init__(self, name: str, duration: int, one_time: bool = False, msg=None):
        self.name = name
        self.duration = duration
        self.one_time = one_time

        if not msg:
            self.msg = f"Now is {self.name} time, you will have to do it for {self.duration} minutes"
        else:
            self.msg = msg

        Task.tasks.append(self)

    def exec(self) -> None:
        # Get the terminal size, progressbar, indentation again so the program is sure that the progress bar is pretty printed even if the user changed the size of the window
        terminal, _, bar = get_terminal_data()

        # Get the indentation for the message printed for the task so it can be middle aligned
        side_space = int((terminal - len(self.msg)) / 2)

        # Print the message of the task middle aligned and say it loud so the user can hear
        print("\n\n")
        print(" " * side_space, self.msg, sep="")
        speak(self.msg)

        # The function that track time and print the progress for the task
        progressbar(self.duration / bar)  # EDITME

    def __str__(self) -> str:
        return f"name: {self.name}, duration: {self.duration}, msg: {self.msg}, one time: {self.one_time}"

    @classmethod
    def save(cls):
        with open("tasks.json", "w") as file:
            dump(
                list(
                    map(
                        lambda task: {
                            "name": task.name,
                            "duration": task.duration,
                            "msg": task.msg,
                        },
                        cls.tasks,
                    )
                ),
                file,
                indent=4,
            )

    @classmethod
    def filter_tasks(cls):
        cls.tasks = list(filter(lambda x: not x.one_time, cls.tasks))

    @classmethod
    def congrats(cls):
        # Congrat the user whenever he finishes a whole set of tasks by pretty printing this message middle aligned and saying it
        cong = "Congratulations, you had just completed a whole loop!"
        l = int((terminal - len(cong)) / 2)
        print(" " * l, cong, sep="")
        speak(cong)

    @classmethod
    def get_tasks(cls, msg: str, one_time: bool = False) -> None:
        while True:
            print(msg)
            speak(msg)

            # The function that takes the tasks from the user
            get_details(one_time)
            break


def get_details(one_time: bool):
    count = 1
    while True:
        task = inputt(f"{count}: ", 5)
        match task:
            case "R":
                Task.tasks = []
                count = 1
                continue
            case "":
                if len(Task.tasks) >= 1:
                    break
                continue
            case _:
                count += 1
                pass
        if one_time or not saved(task, one_time):
            Task(task, get_duration(), one_time)


def progressbar(sleeping):
    print(" " * indent, "_" * bar, sep="")
    print(" " * (indent - 1), "[", sep="", end="")

    for _ in range(bar):
        with open(DO, "r+") as f:
            do = f.read()
            f.truncate(0)
            match do:
                case "p":
                    inputt("", 10)
                    speak("You are having break for ten minutes now! go back to work")
                case "P":
                    inputt("", 30)
                case "f":
                    return
                case _:
                    sleep(sleeping)

        stdout.write("=")
        stdout.flush()

    print("]\n", " " * indent, "_" * bar, "\n\n", sep="")


def saved(shortcut: str, one_time: bool):
    with open(SAVED_TASKS) as file:
        saved_data = load(file)

    if shortcut in saved_data:
        duration = saved_data[shortcut]["duration"]
        print(f"duration is set as defult: {duration}")
    elif shortcut.lower() in saved_data:
        duration = get_duration()
    else:
        return

    obj = saved_data[shortcut.lower()]
    Task(obj["name"], duration, one_time, obj["msg"])
    return True


def get_duration():
    while True:
        try:
            return int(inputt("Duration: ", 1))
        except ValueError:
            continue


def get_terminal_data():
    terminal: int = int(
        str(get_terminal_size()).replace("os.terminal_size(columns=", "").split(",")[0]
    )
    indent: int = int(terminal / 25)
    bar: int = int((terminal / 25) * 23)
    return terminal, indent, bar


def inputt(prompt: str, n: int = 15) -> None:
    try:
        return inputimeout(prompt=prompt, timeout=n * 60)
    except TimeoutOccurred:
        return


def edit_file(key: str) -> None:
    with open(".do", "w") as f:
        f.write(key)


terminal, indent, bar = None, None, None


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        exit()
    except BaseException as e:
        print_exc()
        match inputt("Press enter to search, any key to exit: "):
            case "":
                exit()
            case _:
                popen(f"search {e}")
                exit()

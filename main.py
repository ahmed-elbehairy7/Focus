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

# Get the saved tasks as a global variable
terminal, indent, bar, SAVED_TASKS = [None for _ in range(4)]


def main():
    # Take those global variables to allow editing them for making custom sized progress bar for each task for better visualization
    global terminal, indent, bar

    get_saved_tasks()

    # Get the size of the terminal, progress bar, and the indentation before printing the progress bar
    terminal, indent, bar = get_terminal_data()

    # print an intro for the application
    # print(focus)

    # Make the computer say the following
    speak("Welcome to FOCUS.io")

    Task.get_tasks()

    for task in Task.tasks:
        # Do the task logic
        task.exec()

    # Remove the one time tasks from tasks
    Task.filter_tasks()

    # Forever:
    while True:
        # For each task added by the user
        for task in Task.tasks:
            task.exec()

        Task.congrats()


class Task:
    tasks = []

    def __init__(self, name: str, duration: int, one_time: bool = False, msg=None):
        self.name = name
        self.duration = duration
        self.one_time = one_time

        # If the task doesn't have a message, let it have the default one
        if not msg:
            self.msg = f"Now is {self.name} time, you will have to do it for {self.duration} minutes"
        else:
            self.msg = msg

        Task.tasks.append(self)

    def exec(self) -> None:
        # Get the terminal size, progressbar, indentation again so the program is sure that the progress bar is pretty printed even if the user changed the size of the window
        get_terminal_data()

        # Get the indentation for the message printed for the task so it can be middle aligned
        side_space = int((terminal - len(self.msg)) / 2)

        # Print the message of the task middle aligned and say it loud so the user can hear
        print("\n\n")
        print(" " * side_space, self.msg, sep="")
        speak(self.msg)

        # The function that track time and print the progress for the task
        progressbar(self.duration * 60 / bar)

    def __str__(self) -> str:
        return f"name: {self.name}, duration: {self.duration}, msg: {self.msg}, one time: {self.one_time}"

    @classmethod
    def new_task(cls, one_time: bool, task_input: str) -> None:
        if task_input in SAVED_TASKS:
            Task(
                SAVED_TASKS[task_input]["name"],
                get_duration(one_time, task_input),
                one_time,
                SAVED_TASKS[task_input]["msg"],
            )
        elif task_input.lower() in SAVED_TASKS:
            Task(
                SAVED_TASKS[task_input.lower()]["name"],
                get_duration(),
                one_time,
                SAVED_TASKS[task_input.lower()]["msg"],
            )

        else:
            Task(task_input, get_duration(), one_time)

    @classmethod
    def save(cls) -> None:
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
    def filter_tasks(cls, one_time: bool = True) -> None:
        cls.tasks = list(filter(lambda x: x.one_time != one_time, cls.tasks))

    @classmethod
    def congrats(cls) -> None:
        # Congrat the user whenever he finishes a whole set of tasks by pretty printing this message middle aligned and saying it
        cong = "Congratulations, you had just completed a whole loop!"
        l = int((terminal - len(cong)) / 2)
        print(" " * l, cong, sep="")
        speak(cong)

    @classmethod
    def get_tasks(cls) -> None:
        msgs = {
            True: "Please enter the one time tasks",
            False: "Please enter the looping tasks",
        }
        cls.tasks = []
        one_time = True
        while True:
            msg = msgs[one_time]
            print(msg)
            speak(msg)

            try:
                # The function that takes the tasks from the user
                one_time = get_details(one_time)
                if one_time:
                    map(lambda x: print(x), cls.tasks)
                    return
            except TimeoutOccurred:
                continue


def get_details(one_time: bool) -> bool:
    count = 1
    while True:
        task = inputt(f"{count}: ", 5)
        match task:
            case "R":
                Task.filter_tasks(one_time)
                count = 1
                continue
            case "D":
                return Task.get_tasks()
            case "":
                if len(Task.tasks) >= 1 or one_time:
                    break
                continue
            case _:
                count += 1
                Task.new_task(one_time, task)

    return not one_time


def progressbar(sleeping: int) -> None:
    print(" " * indent, "_" * bar, sep="")
    print(" " * (indent - 1), "[", sep="", end="")

    for _ in range(bar):
        sleep(sleeping)
        stdout.write("=")
        stdout.flush()

    print("]\n", " " * indent, "_" * bar, "\n\n", sep="")


def get_duration(one_time: bool = True, task_input=None) -> int:
    # If the there's no input from the user
    if not task_input:
        while True:
            try:
                return int(inputt("Duration: ", 1))
            except ValueError:
                continue

    try:
        if not one_time:
            duration = SAVED_TASKS[task_input]["durations"]["loop"]
        else:
            duration = SAVED_TASKS[task_input]["durations"]["one_time"]
    except KeyError:
        print("this task does not have a default value duration")
        duration = get_duration()
    print(f"duration set to default: {duration}")
    return duration


def get_terminal_data() -> tuple:
    """The function for pretty printing on terminal"""
    global terminal, indent, bar

    # Get the terminal size
    terminal: int = int(
        str(get_terminal_size()).replace("os.terminal_size(columns=", "").split(",")[0]
    )

    # Know how much should the progress bar be indented and how many '=' to type
    indent: int = int(terminal / 25)
    bar: int = int((terminal / 25) * 23)


def get_saved_tasks() -> None:
    global SAVED_TASKS

    # Open the saved.json file and save it in a global variable
    with open(r"D:\\pam\\focus.io\\saved.json") as file:
        SAVED_TASKS = load(file)

    # Checking that the user doesn't have any keys as R
    keys = [x.lower() for x in SAVED_TASKS.keys()]
    if "r" in keys:
        raise Exception("You can't have the letter 'R' as a shortcut!!")


def inputt(prompt: str, n: int = 15) -> None:
    """
    The function for taking an input with some timeout


    :param str prompt: the prompt of the input
    :param int n: the number of minutes to wait timeout

    :rtype: str
    """
    return inputimeout(prompt=prompt, timeout=n * 60)


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

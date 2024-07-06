from time import sleep
from sys import stdout
from json import dump
from shutil import get_terminal_size
from inputimeout import TimeoutOccurred
from colorama import Fore, Style, Back
from globals import *
from queue import Empty
from command import Command

class Task:
    tasks = []
    SAVED = SAVED['tasks']

    def __init__(self, name: str, duration: int, one_time: bool = False, msg=None):
        self.index = len(Task.tasks)
        self.name = name
        self.duration = duration
        self.one_time = one_time

        # If the task doesn't have a message, let it have the default one
        if not msg:
            self.msg = f"Now is {self.name} time, you will have to do it for {self.duration} minutes"
        else:
            self.msg = msg

        Task.tasks.append(self)

    def exec(self, speak) -> None:
        # Get the terminal size, progressbar, indentation again so the program is sure that the progress bar is pretty printed even if the user changed the size of the window
        get_terminal_data()

        # Get the indentation for the message printed for the task so it can be middle aligned
        side_space = int((terminal - len(self.msg)) / 2)

        # Print the message of the task middle aligned and say it loud so the user can hear
        print("\n\n")
        
        Task.print_tasks(self.index)
        
        Command.print_help()
        print("\n\n")
        
        #msg
        print(" " * side_space, self.msg, sep="")
        speak(self.msg)
        
        # The function that track time and print the progress for the task
        self.progressbar()
    
    
    def progressbar(self) -> None:
        sleeping = self.duration * 60 / bar
        # print(" " * indent, "_" * bar, sep="")
        # print(" " * (indent - 1), "[", sep="", end="")
        print('\n\n', " " * (indent - 1), "|", sep="", end="")

        for _ in range(bar):
            try:
                t = Command.queue.get(True, sleeping)
                match t:
                    case 'p':
                        while True:
                            t = Command.queue.get()
                            if t == 'r':
                                sleep(sleeping)
                                break
                    case 's':
                        return
                    case 'e':
                        raise SystemExit
                    case _:
                        sleep(sleeping)
            except Empty:
                pass
            print(Back.LIGHTWHITE_EX, end='')
            stdout.write(" ")
            stdout.flush()
            print(Style.RESET_ALL, end='')

        print('|\n\n')
        # print("]\n", " " * indent, "_" * bar, "\n\n", sep="")

    
    def __str__(self) -> str:
        return f"name: {self.name}, duration: {self.duration}, msg: {self.msg}, one time: {self.one_time}"


    @classmethod
    def print_tasks(cls, index = None,):
        #print all tasks
        print(Style.DIM, end='')
        for task in Task.tasks:
            if task.one_time:
                name = task.name + "  <>"
            else:
                name = task.name
            if index == task.index:
                print(Style.NORMAL + Fore.LIGHTBLUE_EX + f"{name}" + Fore.WHITE + Style.DIM)
                continue
            print(name)
            
        print(Style.RESET_ALL + '\n')

    @classmethod
    def new_task(cls, one_time: bool, task_input: str) -> None:
        if task_input in cls.SAVED:
            Task(
                cls.SAVED[task_input]["name"],
                cls.get_duration(one_time, task_input),
                one_time,
                cls.SAVED[task_input]["msg"],
            )
        elif task_input.lower() in cls.SAVED:
            Task(
                cls.SAVED[task_input.lower()]["name"],
                cls.get_duration(),
                one_time,
                cls.SAVED[task_input.lower()]["msg"],
            )

        else:
            Task(task_input, cls.get_duration(), one_time)

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
        cls.tasks = cls.filtered_tasks(one_time)
        
    @classmethod
    def filtered_tasks(cls, one_time: bool = True) -> None:
        return list(filter(lambda x: x.one_time != one_time, cls.tasks))

    @classmethod
    def congrats(cls, speak) -> None:
        # Congrat the user whenever he finishes a whole set of tasks by pretty printing this message middle aligned and saying it
        cong = "Congratulations, you had just completed a whole loop!"
        l = int((terminal - len(cong)) / 2)
        print(" " * l,Fore.LIGHTMAGENTA_EX + cong + Style.RESET_ALL, sep="")
        speak(cong)

    @classmethod
    def get_tasks(cls, speak) -> None:
    
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
                one_time = cls.get_details(one_time, speak)
                if one_time:
                    map(lambda x: print(x), cls.tasks)
                    Command.initialize_commands()
                    return
            except TimeoutOccurred:
                continue     


    @classmethod
    def get_details(cls, one_time: bool, speak) -> bool:
        global DELETE_ALL, RESET_TYPE
        while True:
            task = inputt(f"{len(cls.filtered_tasks(not one_time)) + 1}: ", 1)
            if task == RESET_TYPE:
                cls.filter_tasks(one_time)
                continue
            elif task == DELETE_ALL:
                cls.get_tasks(speak)
                return True
            elif task == "":
                if len(cls.tasks) >= 1 or one_time:
                    break
                continue
            else:
                cls.new_task(one_time, task)

        return not one_time

    @classmethod
    def get_duration(cls, one_time: bool = True, task_input=None) -> int:
        # If the there's no input from the user
        if not task_input:
            while True:
                try:
                    value = int(inputt("Duration: ", 1))
                    if value <= 0:
                        continue
                    return value
                except ValueError:
                    continue

        try:
            if not one_time:
                duration = cls.SAVED[task_input]["durations"]["loop"]
            else:
                duration = cls.SAVED[task_input]["durations"]["one_time"]
        except KeyError:
            print("this task does not have a default value duration")
            duration = cls.get_duration()
        print(f"duration set to default: {duration}")
        return duration

def get_terminal_data() -> tuple:
    """The function for pretty printing on terminal"""
    global terminal, indent, bar

    # Get the terminal size
    terminal = int(
        str(get_terminal_size()).replace("os.terminal_size(columns=", "").split(",")[0]
    )

    # Know how much should the progress bar be indented and how many '=' to type
    indent = int(terminal / 25)
    bar = int((terminal / 25) * 23)
    
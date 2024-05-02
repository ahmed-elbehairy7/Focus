#!/usr/bin/python3

from pyttsx3 import speak
from traceback import print_exc
from sys import stdout, exit
from os import popen
from todos import Todo
from tasks import Task
from globals import *
from argparse import ArgumentParser

# ----------------MAIN FUNCTION------------------#
# ----------------MAIN FUNCTION------------------#

parser = ArgumentParser("Focus", description="Application for productivity and focusing without procrastinating")
parser.add_argument("-q", "--quite", action="store_true", help="no ai bot speaking")

args = parser.parse_args()

if args.quite:
    speak = lambda x : ...
    

def main():

    # print an intro for the application
    # print(focus)

    # Make the computer say the following
    speak("Welcome to FOCUS.io")
    
    # Todo.getTodos(speak)

    Task.get_tasks(speak)

    for task in Task.filtered_tasks(False):
        # Do the task logic
        task.exec(speak)

    # Remove the one time tasks from tasks
    Task.filter_tasks()
    
    if not Task.tasks:
        exit()
    
    # Forever:
    while True:
        # For each task added by the user
        for task in Task.tasks:
            task.exec(speak)

        Task.congrats(speak)               


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        exit()
    except BaseException as e:
        print_exc()
        input()
        exit()

#!/usr/bin/python3

speak = lambda _ : _
from traceback import print_exc
from sys import  exit
from tasks import Task

# ----------------MAIN FUNCTION------------------#
# ----------------MAIN FUNCTION------------------#

def main():

    # Make the computer say the following
    speak("Welcome to FOCUS.io")
    
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

from main import *

def main():
    test_filter_tasks()    
    

def test_filter_tasks():
    Task("looping task 1", 16)
    Task("looping task 2", 10)
    Task("one time task 1", 12, True)
    Task("one time task 2", 28, True)
    
    Task.filter_tasks()
    for task in Task.tasks:
        print(task)
    
main()
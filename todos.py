from datetime import datetime
from globals import *
from json import dump

class Todo:
    todos = []
    SAVED : list = SAVED['todos']
    
    def __init__(self, name, start : datetime = datetime.now() , finish : datetime | None = None, done: bool = False) -> None:
        self.name = name
        self.start = start
        self.finish = finish
        self.done = done
        
        Todo.todos.append(self)
    
    def json(self):
        if self.finish:
            finish = self.finish.strftime("%d/%m/%Y, %H:%M:%S")
        else:
            finish = None
        return {
            "name" : self.name,
            "start" : self.start.strftime("%d/%m/%Y, %H:%M:%S"),
            "finish" : None,
            "done" : self.done
        }
    
    def save(self):
        Todo.SAVED.append(self.json())
        SAVED['todos'].append(self.json())
        with open(SAVED_PATH, 'w') as file:
            dump(SAVED, file)
        
    @classmethod
    def listTodos(cls, speak):
        
        for todo in cls.SAVED:
            #print name
            print(f"\n{todo['name']}:", end='   ')
            
            #print finish time
            if todo["finish"]:
                print(todo["finish"], end='   ')
                
            #handle done
            if todo['done']:
                print("✓")
            else:
                print("🇽")
    
    @classmethod    
    def getTodos(cls, speak): 
        while True:
            cls.listTodos(speak)
            todo = input("Add todos? ") 
            match todo:
                case "":
                    return
                case _:
                    match input("add details? "):
                        case "y":
                            Todo(
                                todo, 
                                input("start time: "), 
                                input("finish time: "),
                                False)
                        case _:
                            newTodo = Todo(todo)
                            newTodo.save()
     
# Pamylka focus project

This project is a very simple one for productivity and time management. Using the application is pretty easy, and getting started is way easier.

Although the application have some bugs, but it's good for reminding you with tasks since it literaly talks to you, also for getting most of it, you should add the application to your startup, so when it sees that you didn't enter tasks, it tell you so you're not on auto pilot

## Table of contents

- [Getting started](#getting-started)
  - [setup](#setup)
    - [installing the requirements](#installing-the-requirements)
    - [Making an executable](#making-an-executable)
  - [After running the application](#after-running-the-application)
    - [one time tasks](#one-time-tasks)
    - [looping tasks](#looping-tasks)
    - [reseting tasks](#reseting-tasks)
    - [deleting all tasks](#deleting-all-tasks)
- [saved.json](#savedjson)
- [At the end](#at-the-end)

## Getting started

### setup

#### installing the requirements

The only way right now to use the application is to clone the repo, then install the requirements with this command in the command line.

    pip install -r requirements.txt

<br />
then make sure that the application is working in your device by executing it <code>python main.py</code>.
<br />

#### Making an executable

For making an executable file you can run the following command in the directory where main.py exists

    pyinstaller -F -n focus main.py

> **_NOTE:_** Probably when you try making an executable file, windows will tell you that this is a virus! this is probably becuase the app communicate with some files. Trust me, I'm not trying to hack you by giving you code you can read, but also you should see the code first whenever you want to update it, it's just 200 lines of code!

<br />

### After running the application

#### One time tasks

So, basicly here, the program will ask you for your one time tasks, which are tasks you will do once at the beginning then start studying with your pomodoro timer for example. The program will ask you for them one by one, and when you finish just hit enter
<br />

**You have to tell the application:**

- task name
- task duration

#### looping tasks

so, if you're using pomodoro for studying for example, those will be study for 25 minutes, and break for 5, after typng the name then the duration for every one, hit enter again and it will start with the one time tasks, then loop over the looping tasks

### reseting tasks

So, you made a typo, or the durations is made wrong, just type uppercase R the next time the app asks you for a task. This also means that you cannot use the letter 'R' as a shortcut, so, you can edit [this line of code](https://github.com/ahmed-elbehairy7/Focus/blob/bad46936ca599ac9c3bbe98ad4185da2d4abf8f4/main.py#L16) to change the letter to reset tasks

    RESET_TYPE = "R"

Keep in mind that the reset will only reset the type of tasks you're currently at, to reset all tasks see the following section

### deleting all tasks

simply, in order to delete them all, just type uppercase D as a task, and this will do the job, like before this means that you can't have the letter d as a shortcut, but you can change [this line of code](https://github.com/ahmed-elbehairy7/Focus/blob/bad46936ca599ac9c3bbe98ad4185da2d4abf8f4/main.py#15)

    DELETE_ALL = "D"

## saved.json

Next, you should take a look at the saved.json file, this is the file where you save your common tasks, like daily ones, instead of typing study, duration: 25 every day, you can add a shortuct so for example, when you type s, the program should know that you want to study for 25 minutes, but if you want to study for 15 minutes this day, just enter the s uppercase!

So, let's try it with the data saved right now, open the program and enter q as a task then hit enter. You will notice that it tells you that duration is set to the default value, next one try typing uppercase Q, and the application will ask you for a duration, just put anything for now.

You will notice that the message is differnet from the default one!, also it calls some one named behairy! who's Behairy?! So, the next time you open saved.json, you will find that the shortcut q you just entered is a key for some json object, and this object have this message that were said! so, now you know how to edit this and add your own shortcuts and tasks. I noticed right now that the name do nothing useful for the application but lets just leave it it doesn't bother anyone right?

As you can see, there's two durations, one for looping and the other for one time, you can set one of them or both for each task, but it's not required since the application will handle it and ask you for duration again

If you want to edit the path for the saved.json, edit [this line in code:](https://github.com/ahmed-elbehairy7/Focus/blob/bad46936ca599ac9c3bbe98ad4185da2d4abf8f4/main.py#L17)

    SAVED_TASKS_PATHS = r"D:\\pam\\focus.io\\saved.json"

## At the end

**comming soon إن شاء الله:**

- track applications opened on the pc and yell at the user if he's procrastinating
- open automaticly the applications you use for tasks or setup the environment for you by running some sort of script
- Plays quran at tasks defined that can afford that
- Pausing, skipping tasks...etc. (this existed for a while probably you can find it in older versions, but I wanted to improve it then i messed everything and I'm too lazy to get it back)

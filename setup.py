from pam import BaseApp

focus = BaseApp(
    "focus.io",
    "02.00.00",
    "Productivity",
    "Timer",
    date="19/3/1445",
    application_nu=0,
    wanted_extension="",
)

if __name__ == "__main__":
    print("\n\n")
    focus.printApplication()
    focus.printApps()

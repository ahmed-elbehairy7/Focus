from pam import BaseApp

focus = BaseApp('focus.io', '01.01.01', 'Productivity', 'Timer', date="19/3/1445", application_nu=0, wanted_extension='')

if __name__=="__main__":
    print('\n\n')
    focus.printApplication()
    focus.printApps()

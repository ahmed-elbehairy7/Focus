from inputimeout import inputimeout
from json import load

DELETE_ALL = "D"
RESET_TYPE = "R"
SAVED_PATH = r"D:\\pam\\focus.io\\saved.json"

# Get the saved tasks as a global variable
terminal, indent, bar = [None for _ in range(3)]

file = open(SAVED_PATH)
SAVED = load(file)
file.close()

# Checking that the user doesn't have any keys as R
keys = [x.lower() for x in SAVED['tasks'].keys()]
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
    exit()
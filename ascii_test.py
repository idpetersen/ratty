from pyfiglet import Figlet
from termcolor import colored


f = Figlet(font='isometric2')
print(colored(f.renderText('hello'), 'green'))
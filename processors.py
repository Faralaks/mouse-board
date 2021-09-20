import sys
import time

import pyautogui as pag
import pyperclip as clipboard
from tkinter.messagebox import showerror as error
from tkinter.messagebox import showwarning as warning
import datetime as dt
from os import path
from errors import *

def proc_file_path(file_path: str) -> str:
    file_path = str(file_path)
    if not file_path: raise UnknownError("Bad file path")
    if not path.exists(file_path): raise FileNotExistError("No such file: "+file_path)

    return file_path
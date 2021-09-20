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
    try:
        file_path = str(file_path)
        file_path = path.abspath(file_path) if file_path[0] == "." else file_path
    except:
        raise UnknownError("Can't process file path")
    if not file_path: raise UnknownError("Bad file path")
    if not path.exists(file_path): raise FileNotExistError("No such file: " + file_path)

    return file_path

def proc_x_val(x: str) -> int:
    try:
        x = int(x)
    except Exception as e:
        raise UnknownError("Can't process x value | %s"%e)
    if x < 0: raise BadCoordinateError("x value lower then 0")

    return x

def proc_y_val(y: str) -> int:
    try:
        y = int(y)
    except Exception as e:
        raise UnknownError("Can't process y value | %s"%e)
    if y < 0: raise BadCoordinateError("y value lower then 0")

    return y

def proc_btn_val(btn: str) -> str:
    try:
        btn = str(btn)
    except Exception as e:
        raise UnknownError("Can't process btn value | %s"%e)
    if btn != "left" and btn != "right": raise BadButtonError("btn value must be 'left' or 'right'")

    return btn






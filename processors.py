from os import path
from pyautogui import KEYBOARD_KEYS
from errors import *


def no_proc(val): return val

def proc_file_path(file_path: str) -> str:
    try:
        file_path = str(file_path)
        file_path = path.abspath(file_path) if file_path[0] == "." else file_path
    except:
        raise UnknownError("Can't process file path")
    if not file_path: raise UnknownError("Bad file path")
    if not path.exists(file_path): raise FileNotExistError("No such file: " + file_path)
    return file_path

def proc_i_gt0_val(val: str) -> int:
    try: val = int(val)
    except Exception as e: raise UnknownError("Can't process int value | %s"%e)
    if val < 0: raise ValLT0Error("Int value lower then zero")
    return val

def proc_btn_val(btn: str) -> str:
    try: btn = str(btn)
    except Exception as e: raise UnknownError("Can't process btn value | %s"%e)
    if btn != "left" and btn != "right": raise BadButtonError("btn value must be 'left' or 'right'")
    return btn

def proc_rel_val(val: str) -> int:
    try: val = int(val)
    except Exception as e: raise UnknownError("Can't process relative value | %s"%e)
    return val

def proc_f_gt0_val(val: str) -> float:
    try: val = float(val)
    except Exception as e: raise UnknownError("Can't process float value | %s"%e)
    if val < 0: raise ValLT0Error("Float value lower then zero'")
    return val

def proc_keys(keys: str) -> list:
    try: keys = keys.split()
    except Exception as e: raise UnknownError("Can't process keys string | %s"%e)
    for key in keys:
            if key not in KEYBOARD_KEYS:
                raise BadKeyError("Key %s not available"%key)
    return keys


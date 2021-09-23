from os import path
from pyautogui import KEYBOARD_KEYS
from errors import *


def no_proc(val, _): return val

def proc_file_path(file_path: str, _="") -> str:
    try:
        file_path = str(file_path)
        file_path = path.abspath(file_path) if file_path[0] == "." else file_path
    except Exception as e:
        raise UnknownError("Can't process file path", e)
    if not file_path: raise UnknownError("Bad file path")
    if not path.exists(file_path): raise FileNotExistError(file_path)
    return file_path

def proc_i_gt0_val(val: str, param_name: str="") -> int:
    try: val = int(val)
    except Exception as e: raise UnknownError("Can't process int value", e)
    if val < 0: raise ValLT0Error(val, param_name)
    return val

def proc_btn_val(btn: str, _="") -> str:
    btn = str(btn)
    if btn != "left" and btn != "right": raise BadButtonError(btn)
    return btn

def proc_rel_val(val: str, param_name: str="") -> int:
    try: val = int(val)
    except Exception as e: raise UnknownError("Can't process relative value in parameter %s"%param_name, e)
    return val

def proc_f_gt0_val(val: str, param_name: str="") -> float:
    try: val = float(val)
    except Exception as e: raise UnknownError("Can't process float value", e)
    if val < 0: raise ValLT0Error(val, param_name)
    return val

def proc_confidence(conf: str, _="") -> float:
    try: conf = float(conf)
    except Exception as e: raise UnknownError("Can't process confidence value", e)
    if not (0.0 <= conf <= 1.0): raise BadConfidenceError(conf)
    return conf

def proc_keys(keys: str, _="") -> list:
    try: keys = keys.split()
    except Exception as e: raise UnknownError("Can't process keys string", e)
    for key in keys:
            if key not in KEYBOARD_KEYS:
                raise BadKeyError(key)
    return keys


import datetime as dt
import sys
import time
from os import path

import pyautogui as pag
import pyperclip as clipboard

from errors import *


def paste_text(text):
    buffer = clipboard.paste()
    clipboard.copy(text)
    pag.hotkey("ctrl"if sys.platform=="win32" else "command", "v")
    clipboard.copy(buffer)


def check_file_path(file_path) -> None:
    if not path.exists(file_path):
        raise Exception("No such file: "+file_path)

class Command:
    cmd = ""
    params = None
    param_names = None
    i = 0
    full = ""

    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        self.param_names = param_names
        self.cmd = split[0]
        self.params = split[1:]
        self.full = full
        if len(self.params) == len(param_names):
            self.i = interval
        elif len(self.params)-1 == len(param_names):
            try:
                self.i = float(split[-1])
            except ValueError:
                self.i = interval
        else: raise Exception("Count of given parameters not equal requirement count")


    def __repr__(self) -> str:
        return "cmd: %s, params: %s, i: %d"%(self.cmd, self.params, self.i)

    def log_call(self, add="") -> None:
        print(dt.datetime.now(), self.__repr__()+" "+add)

    def do(self): self.log_call()

    def check(self, processors: dict) -> None:
        print("---", self.full)
        for num, param in enumerate(self.param_names):
            processor = processors.get(param)
            if not processor: raise NoProcessorError(param)
            print(">", param, self.params[num], num)
            try:
                res = processor(self.params[num], param)
                setattr(self, param, res)
            except Exception as e:
                raise Exception(e)


class Wait(Command):
    def __init__(self, split: list=("wait", 0), full: str="", interval: float=0.0, param_names: tuple=()) -> None:
        super().__init__(split, full, interval, param_names)


class Click(Command):
    x = 0
    y = 0
    btn = ""

    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)
                
    def do(self) -> None:
        self.log_call()
        try:
            pag.click(self.x, self.y, 1, 0, self.btn)
        except Exception as e:
            raise UnknownError("Error while doing command: %s" % e)

class Dclick(Command):
    x, y = 0, 0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call()
        try:
            pag.click(self.x, self.y, 2, 0.01, "left")
        except Exception as e:
            raise UnknownError("Error while doing command: %s" % e)


class Write(Command):
    text = ""
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call()
        try:
            paste_text(self.text)
        except Exception as e:
            raise UnknownError("Error while doing command: %s" % e)

class File(Command):
    file_path = ""
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        try:
            with open(self.file_path, "r") as f:
                paste_text(f.read())
        except Exception as e:
            raise UnknownError("Error while doing command: %s"%e)


class Move(Command):
    relative_x, relative_y, time = 0, 0, 0.0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call()
        try:
            pag.move(self.relative_x, self.relative_y, self.time)
        except Exception as e:
            raise UnknownError("Error while doing command: %s"%e)

class Moveto(Command):
    x, y, time = 0, 0, 0.0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call()
        try: pag.moveTo(self.x, self.y, self.time)
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)

class Press(Command):
    keys = []
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call()
        try:
            for key in self.keys:
                pag.keyDown(key)
            for key in self.keys[::-1]:
                pag.keyUp(key)
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)


class Dimage(Command):
    file_path, confidence = "", 0.0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        try:
            self.log_call(add="file_path: " + self.file_path)
            pos = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
            if not pos: raise Exception("No such image on screen")
            x, y = pos[0], pos[1]
            print("   - Try to double click on (%s, %s)" % (x, y))
            pag.click(x, y, 2, 0.01, "left")
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)

class Cimage(Command):
    file_path, btn, confidence, clicks_interval, clicks_count = "", "", 0.0, 0.0, 0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        try:
            self.log_call(add="file_path: " + self.file_path)
            pos = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
            if not pos: raise Exception("No such image on screen")
            x, y = pos[0], pos[1]
            print("   - Try to click on (%s, %s) with %s btn "%(x ,y, self.btn))
            pag.click(x, y, self.clicks_count, self.clicks_interval, self.btn)
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)


class Aimage(Command):
    file_path, btn, confidence, clicks_interval, find_interval, clicks_count = "", "", 0.0, 0.0, 0.0, 0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        try:
            positions = list(pag.locateAllOnScreen(self.file_path, confidence=self.confidence))
            print("   - %s matches were found with the image!"%len(positions))
            for pos in positions:
                x, y = pag.center(pos)
                print("   - Try to click on (%s, %s) with %s btn" % (x, y, self.btn))
                pag.click(x, y, self.clicks_count, self.clicks_interval, self.btn)
                time.sleep(self.find_interval)
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)

class Wimage(Command):
    file_path, confidence, find_interval, time_limit = "", 0.0, 0.0, 0
    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        super().__init__(split, full, interval, param_names)

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        try:
            start_time = dt.datetime.now()
            while True:
                pos = pag.locateOnScreen(self.file_path, confidence=self.confidence)
                if pos: break
                time.sleep(self.find_interval)
                if (dt.datetime.now() - start_time).seconds > self.time_limit: raise TimeLimitReachedError("Image was not found for given time")
        except Exception as e: raise UnknownError("Error while doing command: %s" % e)




FUNCS_AND_PARAMS = {"click": (Click, ("x", "y", "btn")), "dclick": (Dclick, ("x", "y")),
              "move": (Move, ("relative_x", "relative_y", "time")), "moveto": (Moveto, ("x", "y", "time")),
              "write": (Write, ("text",)),
              "file": (File, ("file_path",)),
              "wait": (Wait, ()),
              "press": (Press, ("keys",)),
              "cimage": (Cimage, ("file_path", "confidence", "btn", "clicks_count", "clicks_interval")),
              "aimage": (Aimage, ("file_path", "confidence", "btn", "clicks_count", "clicks_interval", "find_interval")),
              "dimage": (Dimage, ("file_path", "confidence")), "wimage": (Wimage, ("file_path", "confidence", "find_interval", "time_limit"))
              }
import sys
import time

import pyautogui as pag
import pyperclip as clipboard
from tkinter.messagebox import showerror as error
from tkinter.messagebox import showwarning as warning
import datetime as dt
from os import path
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
    processed = {}
    i = 0
    no_i = False
    full = ""

    def __init__(self, split: list, full: str, interval: float, param_names: tuple) -> None:
        self.param_names = param_names
        self.cmd = split[0]
        self.params = split[1:]
        self.full = full
        try:
            self.i = float(split[-1])
        except ValueError:
            self.i = interval
            self.no_i = True

    def __repr__(self) -> str:
        return "cmd: %s, params: %s, i: %d"%(self.cmd, self.params, self.i)

    def log_call(self, add="") -> None:
        print(dt.datetime.now(), self.__repr__()+" "+add)

    def do(self): self.log_call()

    def check(self, processors: dict) -> None:
        print("---", self.full)
        for num, param in enumerate(self.param_names):
            processor = processors.get(param)
            if not processor: NoProcessorError("No processor for parameter name %s"%param)
            print(">", param, self.params[num], num)
            try:
                res = processor(self.params[num])
                setattr(self, param, res)
            except Exception as e:
                raise Error("Err: %s\nLine: %s"%(e, self.full))


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
            pag.click(self.x, self.y, 2, 0.1, "left")
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
    file_path = ""
    confidence = 0.0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence = float(self.params[1])

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        pos = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
        if not pos: raise Exception("No such image on screen")
        x, y = pos[0], pos[1]
        print("   Try to double click on (%s, %s)" % (x, y))
        pag.click(x, y, 2, 0.01, "left")

    def check(self) -> bool:
        self.log_call(add="file_path: " + self.file_path)
        if not path.exists(self.file_path):
            error("No such path like in line", self.full)
            return True
        return False


class Cimage(Command):
    file_path = ""
    confidence = 0.0
    btn = ""
    clicks = 0
    click_i = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence = float(self.params[1])
        self.btn, self.clicks, self.click_i = self.params[2], int(self.params[3]), float(self.params[4])


    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        pos = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
        if not pos: raise Exception("No such image on screen")
        x, y = pos[0], pos[1]
        print("   Try to click on (%s, %s)"%(x ,y))
        pag.click(x, y, self.clicks, self.click_i, self.btn)


    def check(self) -> bool:
        self.log_call(add="file_path: " + self.file_path)
        if not path.exists(self.file_path):
            error("No such path like in line", self.full)
            return True
        if self.btn != "left" and self.btn != "right":
            error("Oh! Wrong button in line", self.full+"\nBad Btn is "+self.btn)
            return True
        return False


class Aimage(Command):
    file_path = ""
    confidence = 0.0
    btn = ""
    clicks = 0
    click_i = 0
    find_i = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence = float(self.params[1])
        self.btn = self.params[2]
        self.clicks, self.click_i, self.find_i = int(self.params[3]), float(self.params[4]), float(self.params[5])


    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        positions = list(pag.locateAllOnScreen(self.file_path, confidence=self.confidence))
        for pos in positions:
            x, y = pag.center(pos)
            print("   Try to click on (%s, %s) with %s btn" % (x, y, self.btn))
            pag.click(x, y, self.clicks, self.click_i, self.btn)
            time.sleep(self.find_i)

    def check(self) -> bool:
        self.log_call(add="file_path: " + self.file_path)
        if not path.exists(self.file_path):
            error("No such path like in line", self.full)
            return True
        if self.btn != "left" and self.btn != "right":
            error("Oh! Wrong button in line", self.full+"\nBad Btn is "+self.btn)
            return True
        if self.clicks < 1:
            error("Oh! Wrong clicks count in line", self.full+"\nBad Count is "+str(self.clicks))
            return True
        if self.click_i < 0:
            error("Oh! Wrong interval between clicks in line", self.full+"\nBad Click Interval is "+str(self.click_i))
            return True
        if self.find_i < 0:
            error("Oh! Wrong  interval between finding picture in line", self.full+"\nBad Find Interval is "+str(self.find_i))
            return True
        return False



class Wimage(Command):
    file_path = ""
    confidence = 0.0
    round_i = 0
    max_wait = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence, self.round_i, self.max_wait = float(self.params[1]), float(self.params[2]), int(self.params[3])

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        while True:
            pos = pag.locateOnScreen(self.file_path, confidence=self.confidence)
            if pos: break
            time.sleep(self.round_i)

    def check(self) -> bool:
        self.log_call(add="file_path: " + self.file_path)
        if not path.exists(self.file_path):
            error("No such path like in line", self.full)
            return True
        return False
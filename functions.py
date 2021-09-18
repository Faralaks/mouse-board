import sys

import pyautogui as pag
import pyperclip as clipboard
from tkinter.messagebox import showerror as error
import datetime as dt
from os import path

def paste_text(text):
    buffer = clipboard.paste()
    clipboard.copy(text)
    pag.hotkey("ctrl"if sys.platform=="win32" else "command", "v")
    clipboard.copy(buffer)

class Command:
    cmd = ""
    params = None
    i = 0
    full = ""

    def __init__(self, split: list, full: str, interval: float) -> None:
        self.cmd = split[0]
        self.params = split[1:]
        self.full = full
        try:
            self.i = float(split[-1])
        except ValueError:
            self.i = interval

    def __repr__(self) -> str:
        return "cmd: %s, params: %s, i: %d"%(self.cmd, self.params, self.i)

    def log_call(self, add="") -> None:
        print(dt.datetime.now(), self.__repr__()+" "+add)


class Click(Command):
    x = 0
    y = 0
    btn = ""


    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.x, self.y, self.btn = int(self.params[0]), int(self.params[1]), self.params[2]
                
    def do(self) -> None:
        self.log_call()
        pag.click(self.x, self.y, 1, 0, self.btn)

    def check(self) -> bool:
        self.log_call()
        if not pag.onScreen(self.x, self.y):
            error("Oh! Wrong point in line", self.full)
            return True
        if self.btn != "left" and self.btn != "right":
            error("Oh! Wrong button in line", self.full)
            return True
        return False


class Write(Command):
    text = ""

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.text = self.params[0]
                
    def do(self) -> None:
        self.log_call()
        paste_text(self.text)
        
    def check(self) -> bool:
        self.log_call()
        return False

class File(Command):
    file_path = ""

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
                
    def do(self) -> None:
        self.log_call(add="file_path: "+self.file_path)
        with open(self.file_path, "r") as f:
            paste_text(f.read())
        
    def check(self) -> bool:
        self.log_call(add="file_path: "+self.file_path)
        if not path.exists(self.file_path):
            error("No such file from line", self.full)
            return True
        return False


class Wait(Command):
    def __init__(self, split: list=("wait", 0), full: str="", interval: float=0.0) -> None:
        super().__init__(split, full, interval)
                
    def do(self) -> None:
        self.log_call()
        
    def check(self) -> bool:
        self.log_call()
        return False


class Dclick(Command):
    x = 0
    y = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.x, self.y = int(self.params[0]), int(self.params[1])

    def do(self) -> None:
        self.log_call()
        pag.click(self.x, self.y, 2, 0.01, "left")

    def check(self) -> bool:
        self.log_call()
        if not pag.onScreen(self.x, self.y):
            error("Oh! Wrong point in line", self.full)
            return True
        return False

class Move(Command):
    x = 0
    y = 0
    slow = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.x, self.y, self.slow = int(self.params[0]), int(self.params[1]), int(self.params[2])

    def do(self) -> None:
        self.log_call()
        pag.move(self.x, self.y, self.slow)

    def check(self) -> bool:
        self.log_call()
        if self.slow < 0:
            error("Oh! Bad Slow parameter in line", self.full)
            return True
        return False


class Moveto(Command):
    x = 0
    y = 0
    slow = 0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.x, self.y, self.slow = int(self.params[0]), int(self.params[1]), int(self.params[2])

    def do(self) -> None:
        self.log_call()
        pag.moveTo(self.x, self.y, self.slow)

    def check(self) -> bool:
        self.log_call()
        if not pag.onScreen(self.x, self.y):
            error("Oh! Wrong point in line", self.full)
            return True
        if self.slow < 0:
            error("Oh! Bad Slow parameter in line", self.full)
            return True
        return False
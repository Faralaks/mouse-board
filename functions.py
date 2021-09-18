import sys
import time

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
    no_i = False
    full = ""

    def __init__(self, split: list, full: str, interval: float) -> None:
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

    def do(self): pass
    def check(self): pass


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
            error("Oh! Bad Slow parameter in line", self.full+"\nBad Slow is "+str(self.slow))
            return True
        return False


class Press(Command):
    keys = []

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.keys = self.params if self.no_i else self.params[:-1]

    def do(self) -> None:
        self.log_call()
        for key in self.keys:
            pag.keyDown(key)
        for key in self.keys[::-1]:
            pag.keyUp(key)

    def check(self) -> bool:
        self.log_call()
        for key in self.keys[::-1]:
            if key not in pag.KEYBOARD_KEYS:
                error("Oh! Bad Key parameter in line", self.full+"\nBad Key is "+key)
                return True
        return False


class Dimage(Command):
    file_path = ""
    confidence = 0.0

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence = float(self.params[1])

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        x, y = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
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

    def __init__(self, split: list, full: str, interval: float) -> None:
        super().__init__(split, full, interval)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
        self.confidence = float(self.params[1])
        self.btn = self.params[2]

    def do(self) -> None:
        self.log_call(add="file_path: " + self.file_path)
        x, y = pag.locateCenterOnScreen(self.file_path, confidence=self.confidence)
        print("   Try to click on (%s, %s)"%(x ,y))
        pag.click(x, y, 1, 0, self.btn)


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
        print(len(positions), positions)
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

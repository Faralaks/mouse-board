import pyautogui as pag
import pyperclip as clipboard
from tkinter.messagebox import showerror as error
import datetime as dt
from os import path

def paste_text(text):
    buffer = clipboard.paste()
    clipboard.copy(text)
    pag.hotkey("ctrl", "v")
    clipboard.copy(buffer)

class Command:
    cmd = ""
    params = None
    i = 0
    full = ""

    def __init__(self, split: list, full: str) -> None:
        self.cmd = split[0]
        self.params = split[1:]
        self.full = full
        try:
            self.i = float(split[-1])
        except ValueError:
            self.i = 0

    def __repr__(self) -> str:
        return "cmd: %s, params: %s, i: %d"%(self.cmd, self.params, self.i)

    def log_call(self, add="") -> None:
        print(dt.datetime.now(), self.__repr__()+" "+add)


class Click(Command):
    x = 0
    y = 0
    btn = ""


    def __init__(self, split: list, full: str) -> None:
        super().__init__(split, full)
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

    def __init__(self, split: list, full: str) -> None:
        super().__init__(split, full)
        self.text = self.params[0]
                
    def do(self) -> None:
        self.log_call()
        paste_text(self.text)
        
    def check(self) -> bool:
        self.log_call()
        return False

class File(Command):
    file_path = ""

    def __init__(self, split: list, full: str) -> None:
        super().__init__(split, full)
        self.file_path = path.abspath(self.params[0]) if self.params[0][0] == "." else self.params[0]
                
    def do(self) -> None:
        self.log_call(add="file_path "+self.file_path)
        with open(self.file_path, "r") as f:
            paste_text(f.read())
        
    def check(self) -> bool:
        self.log_call(add="file_path "+self.file_path)
        if not path.exists(self.file_path):
            error("No such file from line", self.full)
            return True
        return False
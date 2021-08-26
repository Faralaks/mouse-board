import datetime as dt
import os
import sys
import time
import tkinter as tk
from os import path
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename
from tkinter.messagebox import showerror as error

import pyautogui as pag
from PIL import ImageTk

import functions as fn

PATH_SEPARATOR = "\\"if sys.platform=="win32" else "/"
CMD_SEPARATOR = '@'

pag.FAILSAFE = False


log_file = open("log.txt", "a")

sys.stdout = log_file
sys.stderr = log_file
print("\n\n <-------------| Logging Clicker by Faralaks |-------------> \n", dt.datetime.now(), "\n")


class About(tk.Toplevel):
    def __init__(self, parent, photo, write_func):
        super().__init__(parent)
        self.write = write_func
        self.w, self.h = pag.size()
        self.parent = parent
        self.frame = tk.Frame(self)
        self.photo = photo
        self.image = ImageTk.PhotoImage(self.photo)

        
        self.geometry("%sx%s+0+0"%(self.w, self.h))
        self.frame.grid()
        self.focus()


        self.canvas = tk.Canvas(self, height=self.h, width=self.w)
        self.img_obj = self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.grid(row=0, column=0)
        
        self.canvas.bind('<1>', self.click)
        self.bind("<Escape>", self.on_escape)
        
    def on_escape(self, _):
        self.parent.deiconify()
        self.destroy()

    def click(self, event):
        self.write("%s-%s"%(event.x, event.y), with_time=False)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame = tk.Frame(self)
        self.photo = None
        self.frame.grid()
        self.geometry("1550x550+0+-10")
        self.title("Mouse-Board by Faralaks")
        icon = path.join(PATH_SEPARATOR.join(path.split(path.abspath(__file__))[:-1]), "icon.png")

        self.iconphoto(True, tk.PhotoImage(file=icon))
        self.bind("<Escape>", lambda event: self.destroy())

        self.click_interval = "0.1"
        self.macros_interval = "-1"

        self.funcs = {"click":fn.Click, "write":fn.Write, "file":fn.File}

        menu = tk.Menu(self)
        int_menu = tk.Menu(menu)
        menu.add_command(label='Открыть', command=self.load)
        menu.add_command(label='Сохранить', command=self.save)
        int_menu.add_command(label='Между кликами', command=lambda:  self.change_click_int(
                pag.prompt("Стандартный интервал между кликами в секундах, например 1 или 1.5")))
        int_menu.add_command(label='Между запусками', command=lambda: self.change_macros_int(
                pag.prompt("Интервал между перезапуском макроса в минутах, например 10 или 10.5, -1 для отмены автоперезапуска")))
        menu.add_cascade(label="Интервалы", menu=int_menu)
        self.config(menu=menu)

        tk.Button(self.frame, text="RUN Macros", command=self.start_clicking).grid(row=0, column=0)
        tk.Button(self.frame, text="ScreenShot", command=self.open_window).grid(row=0, column=1)
        tk.Button(self.frame, text="Find File", command=self.get_file_path).grid(row=0, column=2)
        self.macros = tk.Text(self.frame, height=25, width=154, wrap=tk.WORD)
        self.macros.grid(row=3, column=0, columnspan=10)


    def change_click_int(self, new_val):
        if not new_val: return
        self.click_interval = new_val

    def change_macros_int(self, new_val):
        if not new_val: return
        self.macros_interval = new_val

    def write_points(self, text, point=tk.END, with_time=True):
        if not with_time: 
            text += CMD_SEPARATOR+self.click_interval
        self.macros.insert(point, text+"\n")

    def save(self):
        f = asksaveasfile(defaultextension=".txt", initialdir=os.getcwd(), mode="w",
                                filetypes=(("Text files","*.txt*"), ("All files", "*.*")))
        if not f: return
        points = self.macros.get(1.0, tk.END).strip()
        f.write(points)
        f.close()

    def get_file_path(self):
        file = askopenfilename(initialdir=os.getcwd(), filetypes = (("Text files","*.txt*"), ("All files", "*.*")))
        if not file: return
        self.write_points(file.replace("/", PATH_SEPARATOR), point=tk.INSERT, with_time=False)

    def load(self):
        self.macros.delete(1.0, tk.END)
        f = askopenfile(initialdir=os.getcwd(), filetypes = (("Text files","*.txt*"), ("All files", "*.*")), mode="r")
        #if not f: return
        points = f.read().strip().split("\n")
        for three in points:
            self.write_points(three)
        f.close()

    def line2cmd(self, line: str) -> [None, fn.Click, fn.Write, fn.File]:
        split = line.split(CMD_SEPARATOR)
        func = self.funcs.get(split[0])
        if not func:
            error("Bad function name in line", line)
            return None
        return func(split, line)

    def start_clicking(self):
        lines = self.macros.get("1.0", tk.END).strip().split("\n")
        commands = list(map(self.line2cmd, lines))
        if None in commands: return
        
        self.wm_state("iconic")
        time.sleep(0.5)

        print("\t @Start checking")
        for command in commands:
            if command.check():
                print("@ERROR in previous line")
                return
        self.deiconify()
        print("\t @Finish checking! No errors!")

        for command in commands:
            command.do()
            time.sleep(command.i)


    def open_window(self):
        self.wm_state("iconic")
        time.sleep(0.5)
        self.photo = pag.screenshot()
        about = About(self, self.photo, self.write_points)
        about.grab_set()



if __name__ == "__main__":
    app = App()
    app.mainloop()
import datetime as dt
import os
import sys
import time
import webbrowser as browser
import tkinter as tk
from os import path
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename
from tkinter.messagebox import showerror as error
from typing import Union

import pyautogui as pag
from PIL import ImageTk
from pyscreeze import locateAll

import functions as fn
import processors as pc
from errors import *

PATH_SEPARATOR = "\\"if sys.platform=="win32" else "/"
PARAM_SEP = '+'

pag.FAILSAFE = False


log_file = open("log.txt", "a")

#sys.stdout = log_file
#sys.stderr = log_file
print("\n\n <-------------| Logging Mouse-Board by Faralaks v3 |-------------> \n", dt.datetime.now(), "\n")


class About(tk.Toplevel):
    def __init__(self, parent, photo, write_func):
        super().__init__(parent)
        self.write = write_func
        self.w, self.h = pag.size()
        self.parent = parent
        self.frame = tk.Frame(self)
        self.photo = photo
        self.image = ImageTk.PhotoImage(self.photo)
        self.mode = tk.StringVar()
        self.image_found = tk.StringVar()
        self.confidence = tk.StringVar()
        self.mode.set("coordinates")
        self.image_found.set("")
        self.confidence.set("0.98")

        
        self.geometry("%sx%s+0+0"%(self.w, self.h))
        self.frame.grid()
        self.focus()

        self.overrideredirect(True)
        tk.Radiobutton(self.frame, text="coordinates", value="coordinates", variable=self.mode, padx=15).grid(row=0, column=0)
        tk.Radiobutton(self.frame, text="click left", value="left", variable=self.mode, padx=15).grid(row=0, column=2)
        tk.Radiobutton(self.frame, text="click right", value="right", variable=self.mode, padx=15).grid(row=0, column=3)
        tk.Radiobutton(self.frame, text="dclick", value="dclick", variable=self.mode, padx=15).grid(row=0, column=4)
        btn_cut = tk.Button(self.frame, text="Cut image", padx=3)
        btn_aimage = tk.Button(self.frame, text="Test aimage", command=self.aimage_preview)
        btn_exit = tk.Button(self.frame, text="Exit", command=self.on_escape)
        btn_aimage.configure(font=("Arial", 8))
        btn_cut.configure(font=("Arial", 8))
        btn_exit.configure(font=("Arial", 8))
        btn_cut.grid(row=0, column=5, padx=25)
        btn_aimage.grid(row=0, column=6)
        tk.Label(self.frame, text="Confidence").grid(row=0, column=7)
        tk.Entry(self.frame, textvariable=self.confidence, width=4).grid(row=0, column=8)
        tk.Label(self.frame, textvariable=self.image_found).grid(row=0, column=9)
        btn_exit.grid(row=0, column=11, padx=25)

        self.canvas = tk.Canvas(self, height=self.h, width=self.w, highlightthickness=1)
        self.img_obj = self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.grid(row=1, column=0)
        
        self.canvas.bind('<1>', self.click)
        self.bind("<Escape>", self.on_escape)
        
    def on_escape(self, _=None):
        self.parent.deiconify()
        self.destroy()

    def aimage_preview(self, _=None, file=None):
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        image_path = askopenfilename(initialdir=os.getcwd()) if not file else file
        if not image_path: return
        confidence = float(self.confidence.get())
        positions = list(locateAll(image_path, self.photo, confidence=confidence))
        self.image_found.set("Found %s"%len(positions))
        for pos in positions:
            center = pag.center(pos)
            self.canvas.create_rectangle(pos[0], pos[1], pos[0]+pos[2], pos[1]+pos[3], outline="red")
            self.canvas.create_rectangle(center[0]-1, center[1]-1, center[0]+1, center[1]+1, fill="green")
        btn_try_again = tk.Button(self.frame, text="Try again", command=lambda: self.aimage_preview(file=image_path))
        btn_try_again.configure(font=("Arial", 8))
        btn_try_again.grid(row=0, column=10)



    def click(self, event: tk.Event):
        mode = self.mode.get()
        if mode == "left" or mode == "right":
            self.write("click%s%s%s%s%s%s" % (PARAM_SEP, event.x, PARAM_SEP, event.y, PARAM_SEP, mode), add_time=True, end="\n")
        elif mode == "dclick":
            self.write("dclick%s%s%s%s" % (PARAM_SEP, event.x, PARAM_SEP, event.y), add_time=True, end="\n")
        else: self.write("%s%s%s" % (event.x, PARAM_SEP, event.y), point=tk.INSERT)



def change_separator(new_val):
    if not new_val: return
    global PARAM_SEP
    PARAM_SEP = new_val


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame = tk.Frame(self)
        self.photo = None
        self.frame.grid()
        self.geometry("1550x620+0+-10")
        self.title("Mouse-Board by Faralaks v3")
        icon = path.join(PATH_SEPARATOR.join(path.split(path.abspath(__file__))[:-1]), "icon.png")

        self.iconphoto(True, tk.PhotoImage(file=icon))
        self.bind("<Escape>", lambda event: self.destroy())

        self.interval = 0.1

        self.funcs = {"click":(fn.Click, ("x", "y", "btn")), "dclick":(fn.Dclick, ("x", "y")),
                      "move":(fn.Move, ("relative_x", "relative_y", "time")), "moveto":(fn.Moveto, ("x", "y", "time")),
                      "write":(fn.Write, ("text",)),
                      "file":(fn.File, ("file_path",)),
                      "wait":(fn.Wait, ()),
                      "press":(fn.Press, ("keys",)),
                      "cimage":(fn.Cimage, ("file_path", "confidence", "btn", "clicks_count", "clicks_interval")),
                      "aimage":(fn.Aimage, ("file_path", "confidence", "btn", "clicks_count", "clicks_interval", "find_interval")),
                      "dimage":(fn.Dimage, ("file_path", "confidence")),  "wimage":(fn.Wimage, ("file_path", "confidence", "find_interval", "time_limit"))
                      }

        self.param_processors = {
            "file_path":pc.proc_file_path,
            "x":pc.proc_i_gt0_val,
            "y":pc.proc_i_gt0_val,
            "clicks_count":pc.proc_i_gt0_val,
            "time_limit":pc.proc_i_gt0_val,
            "btn":pc.proc_btn_val,
            "text":pc.no_proc,
            "clicks_interval":pc.proc_f_gt0_val,
            "find_interval":pc.proc_f_gt0_val,
            "time":pc.proc_f_gt0_val,
            "relative_x":pc.proc_rel_val,
            "relative_y":pc.proc_rel_val,
            "keys":pc.proc_keys,
            "confidence":pc.proc_confidence,
        }

        menu = tk.Menu(self)
        menu.add_command(label='Open', command=self.load)
        menu.add_command(label='Save', command=self.save)
        menu.add_command(label='Interval', command=lambda: self.change_interval(
            pag.prompt("Enter a standard interval between commands in seconds, for example, 1 or 1.5")))
        menu.add_command(label='Separator', command=lambda: change_separator(
            pag.prompt("Enter a new separator, for example, @ or -")))
        menu.add_command(label='Need Help?', command=lambda : browser.open("https://github.com/Faralaks/mouse-board"))
        self.config(menu=menu)

        tk.Button(self.frame, text="RUN Macros", command=self.start_clicking).grid(row=0, column=0)
        tk.Button(self.frame, text="ScreenShot", command=self.open_window).grid(row=0, column=1)
        tk.Button(self.frame, text="Find File", command=self.get_file_path).grid(row=0, column=2)
        self.macros = tk.Text(self.frame, height=25, width=154, wrap=tk.WORD)
        self.macros.configure(font=("Trebuchet MS", 10, "bold"))
        self.macros.grid(row=3, column=0, columnspan=10)


    def change_interval(self, new_val) -> None:
        if not new_val: return
        try:
            self.interval = float(new_val)
        except ValueError:
            error("Invalid interval", "Interval %s can not be float value. Default interval sets to 0.1 sec"%new_val)
            self.interval = 0.1


    def write_in_macros(self, text, point=tk.END, add_time=False, end=""):
        if add_time: 
            text += PARAM_SEP + str(self.interval)
        self.macros.insert(point, text+end)

    def save(self):
        f = asksaveasfile(defaultextension=".txt", initialdir=os.getcwd(), mode="w",
                                filetypes=(("Text files","*.txt*"), ("All files", "*.*")))
        if not f: return
        points = self.macros.get(1.0, tk.END).strip()
        f.write(points)
        f.close()

    def get_file_path(self):
        file = askopenfilename(initialdir=os.getcwd())
        if not file: return
        self.write_in_macros(file.replace("/", PATH_SEPARATOR), point=tk.INSERT, end="")

    def load(self):
        self.macros.delete(1.0, tk.END)
        f = askopenfile(initialdir=os.getcwd(), filetypes = (("Text files","*.txt*"), ("All files", "*.*")), mode="r")
        if not f: return
        lines = f.read().strip().split("\n")
        for line in lines:
            self.write_in_macros(line, end="\n")
        f.close()

    def line2cmd(self, line: str) -> Union[None, fn.Command]:
        if line.strip() == "": return self.funcs["wait"][0](full=line)
        print(line)
        split = line.split(PARAM_SEP)
        func = self.funcs.get(split[0])
        if not func:
            error("Bad function name", line)
            return None
        return func[0](split, line, self.interval, func[1])

    def start_clicking(self):
        lines = self.macros.get("1.0", tk.END).strip().split("\n")
        commands = list(map(self.line2cmd, lines))
        if None in commands: return
        
        self.wm_state("iconic")
        time.sleep(0.5)

        print("\n\t @Start checking")
        for command in commands:
            try:
                command.check(self.param_processors)
            except Error as e:
                print("@ERROR in previous macros line: %s"%e)
                error("Oh! There is some ERROR!", e)
                return
        print("\t @Finish checking! No errors!\n")

        print("\t@Macros START!")
        for command in commands:
            try:
                command.do()
            except Exception as e:
                print("\t@Error while doing macros!: %s"%e)
                return
            time.sleep(command.i)

        print("\t@Macros DONE!")


    def open_window(self):
        self.wm_state("iconic")
        time.sleep(0.5)
        self.photo = pag.screenshot()
        about = About(self, self.photo, self.write_in_macros)
        about.grab_set()



if __name__ == "__main__":
    app = App()
    app.mainloop()
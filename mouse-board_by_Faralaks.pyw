import datetime as dt
import os
import sys
import time
import tkinter as tk
from os import path
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfile, asksaveasfile

import pyautogui as pag
from PIL import ImageTk

pag.FAILSAFE = False


log_file = open("log.txt", "a")

sys.stdout = log_file
sys.stderr = log_file
print("\n\n <-------------| Logging Clicker by Faralaks |-------------> \n", dt.datetime.now(), "\n")


class About(tk.Toplevel):
    def __init__(self, parent, photo, write_func, frame):
        super().__init__(parent)
        self.write = write_func
        self.write_frame = frame
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
        self.write(self.write_frame, "%s-%s"%(event.x, event.y), with_time=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame = tk.Frame(self)
        self.photo = None
        self.frame.grid()
        self.geometry("290x1080+0+0")
        self.title("Clicker by Faralaks")
        icon = path.join("\\".join(path.split(path.abspath(__file__))[:-1]), "icon.png")

        self.iconphoto(True, tk.PhotoImage(file=icon))
        self.bind("<Escape>", lambda event: self.destroy())

        self.points_texts = [None, None]
        self.click_interval = "0.1"
        self.macros_interval = "-1"

        menu = tk.Menu(self)
        int_menu = tk.Menu(menu)
        int_menu.add_command(label='Между кликами', command=lambda:  self.change_click_int(
                                        pag.prompt("Стандартный интервал между кликами в секундах, например 1 или 1.5")))
        int_menu.add_command(label='Между запусками', command=lambda: self.change_macros_int(
                                        pag.prompt("Интервал между перезапуском макроса в минутах, например 10 или 10.5, -1 для отмены автоперезапуска")))
        menu.add_cascade(label="Интервалы", menu=int_menu)
        self.config(menu=menu)

        tk.Button(self.frame, text="Скриншот", command=lambda: self.open_window(0)).grid(row=0, column=0)
        tk.Button(self.frame, text="Сохранить", command=lambda: self.save(0)).grid(row=1, column=0)
        tk.Button(self.frame, text="Открыть", command=lambda: self.load(0)).grid(row=2, column=0)
        tk.Button(self.frame, text="Запустить", command=lambda: self.start_clicking(0)).grid(row=3, column=0)
        self.points_texts[0] = tk.Text(self.frame, width=13, height=50, wrap=tk.WORD)
        self.points_texts[0].grid(row=6, column=0)

        tk.Button(self.frame, text="<<-", command=lambda: self.move_points(1, 0)).grid(row=1, column=1)
        tk.Button(self.frame, text="->>", command=lambda: self.move_points(0, 1)).grid(row=2, column=1)

        tk.Button(self.frame, text="Скриншот", command=lambda: self.open_window(1)).grid(row=0, column=2)
        tk.Button(self.frame, text="Сохранить", command=lambda: self.save(1)).grid(row=1, column=2)
        tk.Button(self.frame, text="Открыть", command=lambda: self.load(1)).grid(row=2, column=2)
        tk.Button(self.frame, text="Запустить", command=lambda: self.start_clicking(1)).grid(row=3, column=2)
        self.points_texts[1] = tk.Text(self.frame, width=13, height=50, wrap=tk.WORD)
        self.points_texts[1].grid(row=6, column=2)

    def change_click_int(self, new_val):
        if not new_val: return
        self.click_interval = new_val

    def change_macros_int(self, new_val):
        if not new_val: return
        self.macros_interval = new_val

    def write_points(self, frame, text, with_time=True):
        if not with_time: 
            text += "-"+self.click_interval
        self.points_texts[frame].insert(tk.END, text+"\n")

    def save(self, frame):
        f = asksaveasfile(defaultextension=".txt", initialdir=os.getcwd(), mode="w", filetypes = (("Text files","*.txt*"), ("All files", "*.*")))
        if not f: return
        points = self.points_texts[frame].get(1.0, tk.END).strip()
        f.write(points)
        f.close()

    def load(self, frame):
        self.points_texts[frame].delete(1.0, tk.END)
        f = askopenfile(initialdir=os.getcwd(), filetypes = (("Text files","*.txt*"), ("All files", "*.*")), mode="r")
        #if not f: return
        points = f.read().strip().split("\n")
        for three in points:
            self.write_points(frame, three)
        f.close()

    def start_clicking(self, frame):
        err = False
        points = self.points_texts[frame].get("1.0", tk.END).strip().split("\n")
        for three in points:
            x, y, i = three.split("-")
            x, y, i = int(x), int(y), float(i)
            if not pag.onScreen(x, y):
                mb.showerror("Слыш, Такой точки нет!", "На экране нет точки с координатами (%s, %s)"%(x, y))
                err = True
            if i < 0:
                mb.showerror("Слыш, Интервал меньше нуля!", "Для точки с координатами (%s, %s) интервал равен %s"%(x, y, i))
                err = True    
        if err: return

        self.wm_state("iconic")
        time.sleep(0.5)

        while True:
            for three in points:
                x, y, i = three.split("-")
                x, y, i = int(x), int(y), float(i)
                pag.click(x, y, 1, 0, "left")
                time.sleep(i)
            if self.macros_interval == "-1": break
            time.sleep(60*float(self.macros_interval))
        
        self.deiconify()
        

    def open_window(self, frame):
        self.wm_state("iconic")
        time.sleep(0.5)
        self.photo = pag.screenshot()
        about = About(self, self.photo, self.write_points, frame)
        about.grab_set()

    def move_points(self, frm, to):
        frm_content = self.points_texts[frm].get(1.0, tk.END).strip().split("\n")
        for three in frm_content:
            self.write_points(to, three)


if __name__ == "__main__":
    app = App()
    app.mainloop()
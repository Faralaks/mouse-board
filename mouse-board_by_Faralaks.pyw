import datetime as dt
import os
import sys
import time
import tkinter as tk
import webbrowser as browser
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror as error

import pyautogui as pag
from PIL import ImageTk
from pyscreeze import locateAll

import functions as fn
import processors as pc
import ui


def EMPTY_FUNC(): pass
PATH_SEPARATOR = "\\"if sys.platform=="win32" else "/"
PARAM_SEP = '+'

pag.FAILSAFE = False


log_file = open("log.txt", "a")

#sys.stdout = log_file
#sys.stderr = log_file
print("\n\n <-------------| Logging Mouse-Board by Faralaks v3 |-------------> \n", dt.datetime.now(), "\n")


show_error = lambda err: error("Oh! There is an ERROR!", err)


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
        self.coord_var = tk.StringVar()
        self.mode.set("coordinates")
        self.image_found.set("")
        self.confidence.set("0.98")
        self.coordinates = None
        self.saved_coordinates = None
        self.on_iteration = EMPTY_FUNC
        self.cut_rect = None

        
        self.geometry("%sx%s+0+0"%(self.w, self.h))
        self.frame.grid()
        self.focus()

        self.overrideredirect(True)
        btn_aimage = tk.Button(self.frame, text="Test aimage", command=self.aimage_preview)
        btn_exit = tk.Button(self.frame, text="Exit", command=self.on_escape, padx=4)
        btn_aimage.configure(font=("Arial", 8))
        btn_exit.configure(font=("Arial", 8))



        tk.Label(self.frame, textvariable=self.coord_var).grid(row=0, column=0)
        tk.Radiobutton(self.frame, text="coordinates", value="coordinates", variable=self.mode, padx=15).grid(row=0, column=1)
        tk.Radiobutton(self.frame, text="click left", value="left", variable=self.mode, padx=15).grid(row=0, column=2)
        tk.Radiobutton(self.frame, text="click right", value="right", variable=self.mode, padx=15).grid(row=0, column=3)
        tk.Radiobutton(self.frame, text="dclick", value="dclick", variable=self.mode, padx=15).grid(row=0, column=4)
        tk.Radiobutton(self.frame, value="cut", variable=self.mode, text="Cut image", padx=15).grid(row=0, column=5)
        btn_aimage.grid(row=0, column=6)
        tk.Label(self.frame, text="Confidence").grid(row=0, column=7)
        tk.Entry(self.frame, textvariable=self.confidence, width=4).grid(row=0, column=8)
        tk.Label(self.frame, textvariable=self.image_found).grid(row=0, column=9)
        btn_exit.grid(row=0, padx=15, column=11)

        self.canvas = tk.Canvas(self, height=self.h, width=self.w, highlightthickness=1)
        self.img_obj = self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.grid(row=1, column=0)
        
        self.canvas.bind('<1>', self.click)
        self.bind("<Escape>", self.on_escape)
        self.bind("<Motion>", self.on_motion)

    def on_escape(self, _=None):
        ui.Window.frame_mapped(self.parent)
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


    def on_motion(self, event: tk.Event):
        self.coordinates = (event.x, event.y)
        self.coord_var.set("x: %s   y: %s"%(event.x, event.y))
        self.on_iteration()

    def draw_rect(self):
        if self.cut_rect: self.canvas.delete(self.cut_rect)
        self.cut_rect = self.canvas.create_rectangle(self.saved_coordinates[0], self.saved_coordinates[1], self.coordinates[0], self.coordinates[1], outline="blue")

    def click(self, event: tk.Event):
        mode = self.mode.get()
        if mode == "left" or mode == "right":
            self.write("click%s%s%s%s%s%s" % (PARAM_SEP, event.x, PARAM_SEP, event.y, PARAM_SEP, mode), add_time=True, end="\n")
        elif mode == "dclick":
            self.write("dclick%s%s%s%s" % (PARAM_SEP, event.x, PARAM_SEP, event.y), add_time=True, end="\n")
        elif mode == "cut":
            if self.saved_coordinates:
                l_cord = min(self.saved_coordinates[0], self.coordinates[0])
                r_cord = max(self.saved_coordinates[0], self.coordinates[0])
                t_cord = min(self.saved_coordinates[1], self.coordinates[1])
                b_cord = max(self.saved_coordinates[1], self.coordinates[1])
                cut = self.photo.crop((l_cord, t_cord, r_cord, b_cord))
                self.on_iteration = EMPTY_FUNC
                self.saved_coordinates = None
                self.canvas.delete(self.cut_rect)

                file = asksaveasfilename(initialdir=os.getcwd(), defaultextension=".jpg", filetypes=(("Image files", "*.jpg*"), ("All files", "*.*")))
                if file: cut.save(file, quality=100)
                return

            self.saved_coordinates = (event.x, event.y)
            self.on_iteration = self.draw_rect

        else: self.write("%s%s%s" % (event.x, PARAM_SEP, event.y), point=tk.INSERT)



def change_separator(new_val):
    if not new_val: return
    global PARAM_SEP
    PARAM_SEP = new_val


class App(ui.Window):
    def __init__(self):
        super().__init__()
        self.photo = None
        self.interval = 0.1
        self.funcs = fn.FUNCS_AND_PARAMS
        self.param_processors = pc.PARAM2PROCESSOR



        ui.Button(self.frame, "RUN Macros", command=self.start_clicking, row=0, column=0)
        ui.Button(self.frame, "ScreenShot", command=self.open_window, row=0, column=1)
        ui.Button(self.frame, "Find File", command=self.get_file_path, row=0, column=2)

        ui.Button(self.frame, row=0, column=3, text='Open', command=self.load)
        ui.Button(self.frame, row=0, column=4, text='Save', command=self.save)
        ui.Button(self.frame, row=0, column=5, text='Interval', command=lambda: self.change_interval(
            pag.prompt("Enter a standard interval between commands in seconds, for example, 1 or 1.5")))
        ui.Button(self.frame, row=0, column=6, text='Separator', command=lambda: change_separator(
            pag.prompt("Enter a new separator, for example, @ or -")))
        ui.Button(self.frame, row=0, column=7, text='Need Help?', command=lambda : browser.open("https://github.com/Faralaks/mouse-board"))

        self.macros = tk.Text(self.frame, height=25, width=154, wrap=tk.WORD, relief="flat", font=("Trebuchet MS", 10, "bold"), bg="#303439", fg="#5da3b3", pady=30)
        self.macros.grid(row=1, column=0, columnspan=15, pady=15)


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

    def line2cmd(self, line: str) -> fn.Command:
        if line.strip() == "": return self.funcs["wait"][0](full=line)
        print(line)
        split = line.split(PARAM_SEP)
        func = self.funcs.get(split[0])
        if not func: raise Exception("Bad function name in line: %s"%line)
        try:
            return func[0](split, line, self.interval, func[1])
        except Exception as e:
            raise Exception("Some problems with building command object \n Error: %s\nLine: %s"%(e, line))

    def start_clicking(self):
        lines = self.macros.get("1.0", tk.END).strip().split("\n")
        try:
            commands = list(map(self.line2cmd, lines))
        except Exception as e:
            show_error(e)
            return

        print("\n\t @Start checking")
        for command in commands:
            try:
                command.check(self.param_processors)
            except Exception as e:
                print("@ERROR in previous macros line: %s"%e)
                error("Oh! There is an ERROR!", "Error: %s\nLine: %s"%(e, command.full))
                return
        print("\t @Finish checking! No errors!\n")

        ui.Window.minimize(self)
        time.sleep(0.5)

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
        ui.Window.minimize(self)
        time.sleep(0.5)
        self.photo = pag.screenshot()
        about = About(self, self.photo, self.write_in_macros)
        about.grab_set()



if __name__ == "__main__":
    app = App()
    app.mainloop()
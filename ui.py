import tkinter as tk

class Frame(tk.Frame):
    def __init__(self, target, bg="#1f2226", height=-1):
        super().__init__(target, bg=bg, padx=20, pady=12, height=height)

class Label(tk.Label):
    def __init__(self, target, text, bg="#1f2226", fg="#02a3c7", font=("Arial", 10, "bold")):
        super().__init__(target, bg=bg, padx=20, pady=12, text=text, fg=fg, font=font)



class Window(tk.Tk):
    frame = None
    title_frame = None
    def __init__(self):
        super().__init__()
        _frame = Frame(self)
        _frame.pack()
        self.frame = Frame(_frame)
        self.title_frame = Frame(_frame, bg="#191c20")
        self.line_frame = Frame(_frame, bg="#4c005f", height=5)


        self.overrideredirect(True)
        self.geometry("1582x775+-10+-10")

        self.close_button = Button(self.title_frame, text='X', command=self.destroy, side=tk.RIGHT, font=("Arial", 7, "bold"))
        self.hide_button = Button(self.title_frame, text='_', command=self.minimize, side=tk.RIGHT, font=("Arial", 7, "bold"))
        Label(self.title_frame, text="Mouse-Board by Faralaks v3", bg="#191c20").pack(side=tk.LEFT)
        self.title_frame.pack(expand=1, fill=tk.X)
        self.line_frame.pack(expand=1, fill=tk.X)
        self.frame.pack(expand=1, fill=tk.BOTH)

        self.title_frame.bind('<B1-Motion>', self.move_window)
        self.bind("<Escape>", lambda _: self.destroy())
        self.title_frame.bind("<Map>", self.frame_mapped)


    def minimize(self, _=None):
        self.update_idletasks()
        self.overrideredirect(False)
        self.state('iconic')

    def frame_mapped(self, _=None):
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')

    def move_window(self, event: tk.Event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

class Button(tk.Button):
    def __init__(self, target, text="", command=None, row=None, column=None, side=None, font=("Arial", 10)):
        super().__init__(target, text=text, command=command, padx=3, fg="#02a3c7", bg='#090a0b', font=font)
        if (row is not None) and (column is not None): self.grid(row=row, column=column)
        elif side is not None: self.pack(side=side, padx=5)
        else: self.pack()


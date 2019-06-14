#!/usr/bin/env python 1
import tkinter as tk
import PhotoBoothClass
from PIL import Image, ImageTk


class UI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        # Creates PhotoboothClass object
        self.core = PhotoBoothClass.PhotoBooth()
        self.attributes('-fullscreen', True)
        self.title("Photo Booth")

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def close_window(self):
        self.destroy()

    def get_screen_size(self):

        print(self.screen_height)
        print(self.screen_width)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        # Allows for JPEG file type to be used
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        image = Image.open("background_image.jpg")
        image = image.resize((int(self.screen_width), self.screen_height))
        self.background_image = ImageTk.PhotoImage(image)
        #self.background_image = tk.PhotoImage(file="background_image.jpg")

        self.background_label = tk.Label(self, image=self.background_image)
        #self.background_label.place(x=0, y=0, width=self.screen_width, height=self.screen_height)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.quit_button = tk.Button(self, text="Quit", justify="center", command=lambda: controller.close_window())
        self.quit_button.place(relx=0.5, rely=0.8)
        self.start_button = tk.Button(self, text="Start", justify="center", command=lambda: controller.show_frame(PageOne))
        self.start_button.place(relx=0.5, rely=0.5)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        # Allows for JPEG file type to be used
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        image = Image.open("background_image.jpg")
        image = image.resize((int(self.screen_width), self.screen_height))
        self.background_image = ImageTk.PhotoImage(image)
        #self.background_image = tk.PhotoImage(file="background_image.jpg")

        self.background_label = tk.Label(self, image=self.background_image)
        #self.background_label.place(x=0, y=0, width=self.screen_width, height=self.screen_height)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.quit_button = tk.Button(self, text="Quit", justify="center", command=lambda: controller.close_window())
        self.quit_button.place(relx=0.5, rely=0.8)
        self.start_button = tk.Button(self, text="Start", justify="center", command=lambda: controller.show_frame(StartPage))
        self.start_button.place(relx=0.5, rely=0.5)

app = UI()
app.mainloop()

# window = tk.Tk()
# window.title("Photo Booth")
# # Code to add widgets will go here...
# window.attributes('-fullscreen', True)

# background_image = tk.PhotoImage(file="backimage.gif")
# background_label = tk.Label(window, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)



# quit_button = tk.Button(window, text="quit", justify="center", command=close_window)
# quit_button.place(relx=0.5, rely=0.8)
# print("no start button")
# start_button = tk.Button(window, text="Start", justify="center", command=app.main_use_case(1))
# print("start_button made")
# start_button.place(relx=0.5, rely=0.5)
# print("start button placed")


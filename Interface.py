#!/usr/bin/env python 1
import tkinter as tk
import PhotoBooth

app = PhotoBooth()


def close_window ():
    window.destroy()


window = tk.Tk()
window.title("Photo Booth")
# Code to add widgets will go here...
window.attributes('-fullscreen', True)

background_image = tk.PhotoImage(file="backimage.gif")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


quit_button = tk.Button(window, text="quit", justify="center", command=close_window)
quit_button.place(relx=0.5, rely=0.8)
start_button = tk.Button(window, text="Start", justify="center", command=app.main_use_case(1))
quit_button.place(relx=0.5, rely=0.5)
window.mainloop()

import tkinter as tk
import PhotoBoothClass
from PIL import Image, ImageTk
from tkinter.ttk import *
#
# class StartPage:
#
#     def __init__(self, master):
#         frameOne = Frame(master)
#         frameOne.pack()
#
#         self.quit_button = Button(frameOne, text="Quit", command=lambda: root.destroy())
#         self.quit_button.pack(side=BOTTOM)
#
#         self.start_button = Button(frameOne, text="Start")
#         self.start_button.pack(side=TOP)
#
#         self.screen_width = frameOne.winfo_screenwidth() / 2
#         self.screen_height = frameOne.winfo_screenheight()
#         master.attributes("-fullscreen", True)
#
#
# root = Tk()
# app = StartPage(root)
# root.mainloop()

# Multi-frame tkinter application v2.3


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

        self.background_choice = 0

        # Creates PhotoboothClass object
        self.core = PhotoBoothClass.PhotoBooth()
        #self.attributes('-fullscreen', True)
        self.title("Photo Booth")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Press Start to Begin").pack(side="top", pady=11, padx=10)
        tk.Button(self, pady=50, text="Start",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Quit",
                  command=master.quit).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="The photographs taken by this photobooth will be saved in the cloud and posted to twitter")\
            .pack(side="top", fill="x", pady=10, padx=10)
        tk.Button(self, text="No I do not",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Yes I do!",
                  command=lambda: master.switch_frame(PageTwo)).pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        text = tk.Label(self, text="Select a background")
        text.pack(side="top", pady=10, padx=10)

        self.backgrounds = []
        self.ImageNumber = 0
        nature_image = Image.open("nature.jpg")
        nature_image = nature_image.resize((300, 300))
        nature_image = ImageTk.PhotoImage(nature_image)

        punk_image = Image.open("punk.jpg")
        punk_image = punk_image.resize((300, 300))
        punk_image = ImageTk.PhotoImage(punk_image)

        space_image = Image.open("spacebackground.jpg")
        space_image = space_image.resize((300, 300))
        space_image = ImageTk.PhotoImage(space_image)

        self.backgrounds.append(nature_image)
        self.backgrounds.append(punk_image)
        self.backgrounds.append(space_image)

        selectButton = tk.Button(self, text="Select", command=lambda: master.switch_frame(PageThree))
        selectButton.pack(side="bottom")

        returnButton = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage))
        returnButton.pack(side="bottom")

        leftArrowImg = tk.PhotoImage(file='arrowleft.png')
        leftArrowImg = leftArrowImg.subsample(2,2)
        leftButton = tk.Button(self, image=leftArrowImg, command=lambda: self.changeBackgroundImage(-1))
        leftArrowImg.image = leftArrowImg
        leftButton.pack(side="left")

        rightArrowImg = tk.PhotoImage(file='arrowright.png')
        rightArrowImg = rightArrowImg.subsample(2, 2)
        rightButton = tk.Button(self,image=rightArrowImg, command=lambda: self.changeBackgroundImage(1))
        rightButton.image = rightArrowImg
        rightButton.pack(side="right")

        self.label = tk.Label(self, image=self.backgrounds[self.ImageNumber])
        self.label.image = self.backgrounds[0]
        self.label.pack()

    def changeBackgroundImage(self, choice):
        app.background_choice += choice
        if app.background_choice == len(self.backgrounds):
            app.background_choice = 0
        if app.background_choice == -1:
            app.background_choice = len(self.backgrounds)-1
        self.label.configure(image=self.backgrounds[app.background_choice])


class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        text = tk.Label(self, text="Preview")
        text.pack(side="top", pady=10, padx=10)
        app.core.camera.open_window()


if __name__ == "__main__":
    app = App()
    app.mainloop()

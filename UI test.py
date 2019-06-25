import tkinter as tk
import PhotoBoothClass
from PIL import Image, ImageTk
import time


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

        self.background_choice = 0

        # Creates PhotoboothClass object
        self.core = PhotoBoothClass.PhotoBooth()
        self.attributes('-fullscreen', True)
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
        tk.Button(self, text="No I do not", command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Yes I do!", command=lambda: master.switch_frame(PageTwo)).pack()


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
        leftButton.image = leftArrowImg
        leftButton.pack(side="left")

        rightArrowImg = tk.PhotoImage(file='arrowright.png')
        rightArrowImg = rightArrowImg.subsample(2, 2)
        rightButton = tk.Button(self, image=rightArrowImg, command=lambda: self.changeBackgroundImage(1))
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
        self.countdown_images = []
        temp = Image.open("1.png")
        self.image_1 = ImageTk.PhotoImage(temp)
        temp = Image.open("2.png")
        self.image_2 = ImageTk.PhotoImage(temp)
        temp = Image.open("3.png")
        self.image_3 = ImageTk.PhotoImage(temp)

        self.countdown_images.append(self.image_3)
        self.countdown_images.append(self.image_2)
        self.countdown_images.append(self.image_1)

        self.count = 0

        # Creating canvas. Used so the place manager can be used
        self.w = tk.Canvas(self, bg='pink', width=800, height=480)
        self.w.pack()
        self.ready_button = tk.Button(self.w, text="Begin \nCountdown", command=lambda: self.countdown())
        self.ready_button.config(height=15, width=17)
        self.ready_button.place(x=640, y=50)
        self.back_button = tk.Button(self.w, text="Back", command=lambda: [app.switch_frame(PageTwo),
                                                                           self.w.delete("all")])
        self.back_button.config(height=5, width=17)
        self.back_button.place(x=640, y=330)
        self.countdown_label = tk.Label(self.w, image=self.countdown_images[0], bg='pink', height=400, width=200)
        app.core.camera.open_window()

    def countdown(self):

        def countdown_timer():
            if self.count == 3:
                print("done")
                return
            self.countdown_label.configure(image=self.countdown_images[self.count])
            self.countdown_label.photo = self.countdown_images[self.count]
            self.countdown_label.place(x=620, y=50)
            self.count += 1
            print(self.count)
            app.after(1000, countdown_timer)

        self.ready_button.place_forget()
        self.back_button.place_forget()
        self.countdown_label.place(x=640, y=50)
        app.after(0, countdown_timer)


if __name__ == "__main__":
    app = App()
    app.mainloop()

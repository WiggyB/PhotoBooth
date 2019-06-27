import tkinter as tk
import PhotoBoothClass
from PIL import Image, ImageTk
import time

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

        # Creates PhotoBoothClass object
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
        tk.Label(self, text="The photographs taken by this photo booth will be saved in the cloud"
                            " and posted to twitter").pack(side="top", fill="x", pady=10, padx=10)
        tk.Button(self, text="No I do not", command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Yes I do!", command=lambda: master.switch_frame(PageTwo)).pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        text = tk.Label(self, text="Select a background")
        text.pack(side="top", pady=10, padx=10)

        select_button = tk.Button(self, text="Select", command=lambda: master.switch_frame(PageThree))
        select_button.pack(side="bottom")

        return_button = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage))
        return_button.pack(side="bottom")

        left_arrow_img = tk.PhotoImage(file='arrowleft.png')
        left_arrow_img = left_arrow_img.subsample(2, 2)
        left_button = tk.Button(self, image=left_arrow_img, command=lambda: self.change_background_image(-1))
        left_button.image = left_arrow_img
        left_button.pack(side="left")

        right_arrow_img = tk.PhotoImage(file='arrowright.png')
        right_arrow_img = right_arrow_img.subsample(2, 2)
        right_button = tk.Button(self, image=right_arrow_img, command=lambda: self.change_background_image(1))
        right_button.image = right_arrow_img
        right_button.pack(side="right")

        self.label = tk.Label(self, image=master.core.backgrounds_preview[master.core.ImageNumber])
        self.label.image = master.core.backgrounds_preview[master.core.ImageNumber]
        self.label.pack()

    def change_background_image(self, choice):
        app.core.background_choice += choice
        if app.core.background_choice == len(self.master.core.backgrounds_preview):
            app.core.background_choice = 0
        if app.core.background_choice == -1:
            app.core.background_choice = len(self.master.core.backgrounds_preview)-1
        self.label.configure(image=self.master.core.backgrounds_preview[app.core.background_choice])


class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.countdown_images = []
        for x in range(3, 0, -1):
            print(x)
            self.countdown_images.append(ImageTk.PhotoImage(Image.open(str(x) + '.png')))
            #temp = Image.open("1.png")
            #self.image_1 = ImageTk.PhotoImage(temp)
            #temp = Image.open("2.png")
            #self.image_2 = ImageTk.PhotoImage(temp)
            #temp = Image.open("3.png")
            #self.image_3 = ImageTk.PhotoImage(temp)

            #self.countdown_images.append(self.image_3)
            #self.countdown_images.append(self.image_2)
            #self.countdown_images.append(self.image_1)

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
        print(len(self.countdown_images))
        self.countdown_label = tk.Label(self.w, image=self.countdown_images[0], bg='pink', height=400, width=200)
        app.core.camera.open_window()

    def countdown(self):

        def countdown_timer():
            if self.count == 3:
                start = time.time()
                app.switch_frame(PageFour)
                switchFrame = time.time()
                print("change frame: " + str(switchFrame - start))
                # app.core.take_picture()
                end = time.time()
                print("change take_picture: " + str(end - switchFrame))
                return
            self.countdown_label.configure(image=self.countdown_images[self.count])
            self.countdown_label.photo = self.countdown_images[self.count]
            self.countdown_label.place(x=620, y=50)
            self.count += 1
            app.after(1000, countdown_timer)

        self.ready_button.place_forget()
        self.back_button.place_forget()
        self.countdown_label.place(x=640, y=50)
        app.after(0, countdown_timer)


class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.loading_label = tk.Label(master, text="Loading...")
        self.loading_label.place(relx=0.5, rely=0.5, anchor='center')
        app.core.take_picture()


class PageFive(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.picture = tk.Label(master)


if __name__ == "__main__":
    app = App()
    app.mainloop()

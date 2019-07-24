import tkinter as tk
from tkinter.ttk import Progressbar
import PhotoBoothClass
from PIL import Image, ImageTk
import time
import threading


# Master TK object
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

        # Creates PhotoBoothClass object
        self.core = PhotoBoothClass.PhotoBooth()
        self.attributes('-fullscreen', True)
        self.title("Photo Booth")
        self.start = 0
        self.end = 0

    # Destroys current frame object and replaces it with a new one
    def switch_frame(self, frame_class):
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
                            " and posted to twitter \n Do you consent to this?").pack(side="top", fill="x",
                                                                                      pady=10, padx=10)
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

        left_arrow_img = tk.PhotoImage(file='images/arrowleft.png')
        left_arrow_img = left_arrow_img.subsample(2, 2)
        left_button = tk.Button(self, image=left_arrow_img, command=lambda: self.change_background_image(-1))
        left_button.image = left_arrow_img
        left_button.pack(side="left")

        right_arrow_img = tk.PhotoImage(file='images/arrowright.png')
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
            self.countdown_images.append(ImageTk.PhotoImage(Image.open("images/" + str(x) + '.png')))

        self.count = 0

        # Creating canvas. A canvas is used so we can use the place manager.
        # This is required due to the preview screen being shown above the GUI
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

        # Starts the countdown to take the picture, changes displayed image
        # the "after" method is used because time.sleep() would stop the TK mainloop as well, freezing the whole app
        def countdown_timer():
            if self.count == 3:
                self.master.start = time.time()
                self.master.switch_frame(PageFour)
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
        self.w = tk.Canvas(self, bg='pink', width=800, height=480)
        self.w.pack()
        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='determinate',
                                        maximum=self.master.core.image_size[1])
        self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')

        self.quitButton = tk.Button(self.w, text="Quit", command=master.quit, pady=20, padx=20)
        self.quitButton.place(relx=0.5, rely=0.7, anchor='center')

        # Starts the Image processing in a separate thread so the GUI is responsive
        threading.Thread(target=self.threading_picture).start()

    def threading_picture(self):
        app.core.take_picture(self, self.progress_bar)
        return

    def process_complete(self):
        self.master.switch_frame(PageFive)


class PageFive(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        processed_photo = Image.open(self.master.core.get_merge_path())
        processed_photo = processed_photo.resize((640, 360))
        processed_photo = ImageTk.PhotoImage(processed_photo)

        self.picture = tk.Label(self, image=processed_photo)
        self.picture.image = processed_photo
        self.picture.pack()
        self.start_button = tk.Button(self, text="Start Again", command=master.switch_frame(StartPage),
                                      pady=20, padx=20)
        self.start_button.pack()
        self.quit_button = tk.Button(self, text="Quit", command=master.quit, pady=20, padx=20)
        self.quit_button.pack()


# Start main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

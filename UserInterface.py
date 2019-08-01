import tkinter as tk
from tkinter.ttk import Progressbar
import PhotoBoothClass
from PIL import Image, ImageTk
import time
import threading


class TkThread:
    def __init__(self):
        self.app = App()
        #self.message_queue = queue.Queue()
        #self.message_event = '<<message>>'
        #self.app.bind(self.message_event, self.process_message_queue)

    def run_tk(self):
        self.app.mainloop()

    def send_message_to_ui(self, message):
        #self.message_queue.put(message)
        #self.app.event_generate(self.message_event, when='tail')
        return

    def process_message_queue(self, event):
        #while self.message_queue.empty() is False:
        #    message = self.message_queue.get(block=False)
        #    # process the message here
        return


class BackgroundThread:

    def __init__(self, ui_thread):
        self.tk_thread = ui_thread
        self.thread = threading.Thread(target=self.run_thread)
        self.thread.start()

    def run_thread(self):
        photo_booth.take_picture(self.tk_thread)


# Master TK object
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(StartPage)

        # self.attributes('-fullscreen', True)
        self.title("Photo Booth")
        self.start = 0
        self.end = 0
        self.count = 0
        self.merged_image = None

    def set_merged_image(self, image):
        self.merged_image = image

    # Destroys current frame object and replaces it with a new one
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()

    # Starts the countdown to take the picture, changes displayed image
    # the "after" method is used because time.sleep() would stop the TK mainloop as well, freezing the whole app
    def countdown_timer(self):
        if self.count == 3:
            self.start = time.time()
            self.switch_frame(PageFour)
            self.count = 0
            return

        self.frame.countdown_label.configure(image=self.frame.countdown_images[self.count])
        self.frame.countdown_label.photo = self.frame.countdown_images[self.count]
        self.frame.countdown_label.place(x=620, y=50)
        self.count += 1
        self.after(1000, self.countdown_timer)

    # Called by background thread to move to next frame
    def show_picture(self):
        self.switch_frame(PageFive)


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

        self.label = tk.Label(self, image=photo_booth.backgrounds_preview[photo_booth.ImageNumber])
        self.label.image = photo_booth.backgrounds_preview[photo_booth.ImageNumber]
        self.label.pack()

    def change_background_image(self, choice):
        photo_booth.background_choice += choice
        if photo_booth.background_choice == len(photo_booth.backgrounds_preview):
            photo_booth.background_choice = 0
        if photo_booth.background_choice == -1:
            photo_booth.background_choice = len(photo_booth.backgrounds_preview)-1
        self.label.configure(image=photo_booth.backgrounds_preview[photo_booth.background_choice])


class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.countdown_images = []
        for x in range(3, 0, -1):
            self.countdown_images.append(ImageTk.PhotoImage(Image.open("images/" + str(x) + '.png')))

        # Creating canvas. A canvas is used so we can use the place manager.
        # This is required due to the preview screen being shown above the GUI
        self.w = tk.Canvas(self, bg='pink', width=800, height=480)
        self.w.pack()
        self.ready_button = tk.Button(self.w, text="Begin \nCountdown", command=lambda: self.master.after(0, self.master.countdown_timer))
        self.ready_button.config(height=15, width=17)
        self.ready_button.place(x=640, y=50)
        self.back_button = tk.Button(self.w, text="Back", command=lambda: [self.master.switch_frame(PageTwo),
                                                                           self.w.delete("all")])
        self.back_button.config(height=5, width=17)
        self.back_button.place(x=640, y=330)
        self.countdown_label = tk.Label(self.w, image=self.countdown_images[0], bg='pink', height=400, width=200)
        photo_booth.camera.open_window()


class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.w = tk.Canvas(self, bg='pink', width=800, height=480)
        self.w.pack()
        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, length=500, mode='indeterminate')
        self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.progress_bar.start()
        self.quitButton = tk.Button(self.w, text="Quit", command=master.quit, pady=20, padx=20)
        self.quitButton.place(relx=0.5, rely=0.7, anchor='center')
        self.master.after(0, self.threading_picture)
        # Starts the Image processing in a separate thread so the GUI is responsive
        # threading.Thread(target=self.threading_picture).start()

    @staticmethod
    def threading_picture():
        BackgroundThread(tk_thread)


class PageFive(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #processed_photo = Image.open(self.master.core.get_merge_path())
        self.master.merged_image = self.master.merged_image.resize((640, 360))
        self.master.merged_image = ImageTk.PhotoImage(self.master.merged_image)
        #processed_photo = processed_photo.resize((640, 360))

        self.picture = tk.Label(self, image=self.master.merged_image)
        self.picture.image = self.master.merged_image
        self.picture.pack()
        self.start_button = tk.Button(self, text="Start Again", command=lambda: master.switch_frame(StartPage),
                                      pady=20, padx=20)
        self.start_button.pack()
        self.quit_button = tk.Button(self, text="Quit", command=master.quit, pady=20, padx=20)
        self.quit_button.pack()


# Start main loop
if __name__ == "__main__":
    tk_thread = TkThread()
    photo_booth = PhotoBoothClass.PhotoBooth() # Creates PhotoBoothClass object

    tk_thread.run_tk()  # initiate last, since this runs tk.main_loop() which is a blocking call


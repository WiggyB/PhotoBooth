import tkinter as tk
from tkinter.ttk import Progressbar, Style
import PhotoBoothClass
from PIL import Image, ImageTk
import threading
import os


# Object that processes images in the background, allowing concurrency
class BackgroundThread:

    def __init__(self, ui_thread, kind):

        self.kind = kind
        self.tk_thread = ui_thread
        if kind == "preview":
            self.thread = threading.Thread(target=self.run_preview_thread)
            self.thread.start()
        else:
            self.thread = threading.Thread(target=self.run_full_thread)
            self.thread.start()

    def run_preview_thread(self):
        photo_booth.take_picture(self.tk_thread)

    def run_full_thread(self):
        photo_booth.accept_picture(self.tk_thread)


# Master TK object
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.font = ('dyuthi', 40, 'bold')
        self.button_font = ('dyuthi', 30, 'bold')
        self.frame = None
        self.attributes('-fullscreen', True)
        # Makes cursor invisible on Raspberry Pi
        if os.uname()[4][:3] == 'arm':
            self.config(cursor='none')
        self.title("Photo Booth")
        self.count = 0
        self.merged_image = None
        self.bg_colour = "#666B6A"  # icon colour #660099 need to make the icons
        self.text_colour = '#660099'
        self.button_bg_colour = "#8D5A97"

        self.countdown_images = []
        for x in range(3, 0, -1):
            self.countdown_images.append(ImageTk.PhotoImage(Image.open("images/" + str(x) + '.png')))

        # Create first frame
        self.switch_frame(StartPage)

    def set_merged_preview(self, image):
        self.merged_image = image

    # Destroys current frame object and replaces it with a new one
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(expand=True, fill='both')

    # Starts the countdown to take the picture, changes displayed image
    # the "after" method is used because time.sleep() would stop the TK mainloop as well, freezing the whole app
    def countdown_timer(self):
        if self.count == 3:
            self.switch_frame(PageFour)
            self.count = 0
            return

        self.frame.countdown_label.configure(image=self.countdown_images[self.count])
        self.frame.countdown_label.photo = self.countdown_images[self.count]
        self.frame.countdown_label.place(x=620, y=50)
        self.count += 1
        self.after(1500, self.countdown_timer)

    # Called by background thread to move to next frame
    def show_picture(self):
        self.switch_frame(PageFive)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)
        self.label = tk.Label(self, text="Press Start to Begin", bg=master.bg_colour, fg=master.text_colour)
        self.label.pack(side="top", expand=True, fill='both')
        self.label.config(font=master.font)
        start_img = tk.PhotoImage(file='images/start.png')
        self.start_button = tk.Button(self, bg=master.bg_colour, highlightthickness=0, font=master.button_font,
                                      relief="flat", activebackground=master.bg_colour, image=start_img,
                                      command=lambda: master.switch_frame(PageTwo))
        self.start_button.image = start_img
        self.start_button.pack(side="left", expand=True, fill="both")


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)

        self.label = tk.Label(self, text="Do you consent to this image\n being posted to twitter?", bg=master.bg_colour,
                              fg=master.text_colour)
        self.label.pack(side="top", expand=True, fill="both")
        self.label.config(font=master.button_font)
        no_cross = tk.PhotoImage(file='images/no_cross.png')
        self.no_button = tk.Button(self, highlightthickness=0, bg=master.bg_colour, activebackground=master.bg_colour,
                                   image=no_cross, relief="flat", command=lambda: master.switch_frame(StartPage))
        self.no_button.pack(side="right", expand=True, fill="both", pady=20)
        self.no_button.image = no_cross
        yes_tick = tk.PhotoImage(file='images/yes_tick.png')
        self.yes_button = tk.Button(self, highlightthickness=0, bg=master.bg_colour, activebackground=master.bg_colour,
                                    image=yes_tick, relief="flat", command=lambda: master.switch_frame(PageTwo))
        self.yes_button.image = yes_tick
        self.yes_button.pack(side="left", expand=True, fill="both", pady=20)


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)
        self.button_canvas = tk.Canvas(self, bg=master.bg_colour, highlightthickness=0)
        self.button_canvas.pack(side='top', fill='x')
        self.select_canvas = tk.Canvas(self, bg=master.bg_colour, highlightthickness=0)
        self.select_canvas.pack(side='top', fill='both', expand=True)
        self.label = tk.Label(self.button_canvas, text="Select a background", bg=master.bg_colour,
                              fg=master.text_colour)
        self.label.pack(side="right", expand=True)
        self.label.config(font=master.font)

        back_arrow = tk.PhotoImage(file='images/back_arrow.png')
        self.back_button = tk.Button(self.button_canvas, highlightthickness=0, activebackground=master.bg_colour,
                                     relief="flat", image=back_arrow, bg=master.bg_colour,
                                     command=lambda: master.switch_frame(StartPage))
        self.back_button.image = back_arrow
        self.back_button.pack(side="left", fill="x")

        left_arrow_img = tk.PhotoImage(file='images/arrowleft.png')
        left_arrow_img = left_arrow_img.subsample(2, 2)
        self.left_button = tk.Button(self.select_canvas, bg=master.bg_colour, highlightthickness=0,
                                     activebackground=master.bg_colour, image=left_arrow_img, relief="flat",
                                     command=lambda: self.change_background_image(-1))
        self.left_button.image = left_arrow_img
        self.left_button.pack(side="left", fill="x")

        right_arrow_img = tk.PhotoImage(file='images/arrowright.png')
        right_arrow_img = right_arrow_img.subsample(2, 2)
        self.right_button = tk.Button(self.select_canvas, bg=master.bg_colour, highlightthickness=0,
                                      activebackground=master.bg_colour, image=right_arrow_img, relief="flat",
                                      command=lambda: self.change_background_image(1))
        self.right_button.image = right_arrow_img
        self.right_button.pack(side="right")

        self.image = tk.Button(self.select_canvas, borderwidth=0, relief='flat', bg=master.bg_colour,
                               image=photo_booth.backgrounds_select[photo_booth.imageNumber],
                               highlightthickness=0, activebackground=master.bg_colour,
                               command=lambda: master.switch_frame(PageThree))
        self.image.image = photo_booth.backgrounds_select[photo_booth.imageNumber]
        self.image.pack()

    # Records selection of background image and updates display
    def change_background_image(self, choice):
        photo_booth.background_choice += choice
        if photo_booth.background_choice == len(photo_booth.backgrounds_select):
            photo_booth.background_choice = 0
        if photo_booth.background_choice == -1:
            photo_booth.background_choice = len(photo_booth.backgrounds_select)-1
        self.image.configure(image=photo_booth.backgrounds_select[photo_booth.background_choice])


class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)
        ready_img = tk.PhotoImage(file='images/ready.png')
        self.ready_button = tk.Button(self, bg=master.bg_colour, activebackground=master.bg_colour, relief='flat',
                                      highlightthickness=0, image=ready_img,
                                      command=lambda: self.master.after(0, self.master.countdown_timer))
        self.ready_button.image = ready_img
        self.ready_button.place(x=656, y=50)
        back_arrow = tk.PhotoImage(file='images/back_arrow.png')
        self.back_button = tk.Button(self, bg=master.bg_colour, activebackground=master.bg_colour, highlightthickness=0,
                                     image=back_arrow, relief='flat',
                                     command=lambda: [self.master.switch_frame(PageTwo),
                                                      photo_booth.camera.close_window()])
        self.back_button.image = back_arrow
        self.back_button.place(x=656, y=330)
        self.countdown_label = tk.Label(self, image=master.countdown_images[0], bg=master.bg_colour,
                                        height=500, width=200)
        # Creates preview window
        photo_booth.camera.open_window()


class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)
        s = Style()
        s.theme_use('clam')
        s.configure("purple.Horizontal.TProgressbar", foreground=master.bg_colour, background='#660099')
        self.license_text = tk.Label(self, text="Icon made by Freepik from www.flaticon.com", bg=master.bg_colour)
        self.license_text.place(relx=0.5, rely=0.9, anchor='center')
        self.progress_bar = Progressbar(self, style="purple.Horizontal.TProgressbar", orient=tk.HORIZONTAL, length=500,
                                        mode='indeterminate')
        self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.progress_bar.start()
        self.master.after(0, self.threading_picture_preview)

    # Starts the Image processing in a separate object so the GUI is responsive
    def threading_picture_preview(self):
        BackgroundThread(self.master, "preview")


class PageFive(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=master.bg_colour)

        self.master.merged_image = ImageTk.PhotoImage(self.master.merged_image)
        self.picture = tk.Label(self, image=self.master.merged_image, bg=master.bg_colour)
        self.picture.image = self.master.merged_image
        self.picture.pack(side='left')

        self.button_canvas = tk.Canvas(self, bg=master.bg_colour, highlightthickness=0)
        self.button_canvas.pack(side='right')

        retry_button_img = tk.PhotoImage(file='images/retry_button.png')
        self.retry_button = tk.Button(self.button_canvas, bg=master.bg_colour, activebackground=master.bg_colour,
                                      highlightthickness=0, image=retry_button_img, relief='flat',
                                      command=lambda: master.switch_frame(PageThree))
        self.retry_button.image = retry_button_img
        self.retry_button.pack(side="top", pady=50, padx=(0, 10))

        confirm_button = tk.PhotoImage(file='images/confirm_button.png')
        self.confirm_button = tk.Button(self.button_canvas, bg=master.bg_colour, activebackground=master.bg_colour,
                                        highlightthickness=0, image=confirm_button, relief='flat',
                                        command=lambda: [self.threading_picture_full(), master.switch_frame(StartPage)])
        self.confirm_button.image = confirm_button
        self.confirm_button.pack(side='left', pady=50, padx=(0, 10))

    # Starts the Image processing in a separate object so the GUI is responsive
    def threading_picture_full(self):
        BackgroundThread(self.master, "full")


# Start main loop
if __name__ == "__main__":
    os.chdir('/home/pi/Desktop/TM470_Project')
    app = App()
    photo_booth = PhotoBoothClass.PhotoBooth()  # Creates PhotoBoothClass object
    app.mainloop()

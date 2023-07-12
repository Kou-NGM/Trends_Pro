# File: window2.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

class SecondWindow:
    def __init__(self, root, back_callback, next_callback, last_directory_path=None):
        self.frame = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.back_callback = back_callback
        self.next_callback = next_callback

        # Load the image and resize it to fit the window
        image = Image.open("assets/image1.JPG")
        image = image.resize((int(root.winfo_screenwidth()//3), int(root.winfo_screenheight()*0.8)), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Create a label to hold the image and add it to the left side of the PanedWindow
        image_label = tk.Label(self.frame, image=image)
        image_label.image = image
        self.frame.add(image_label)

        # Create a frame to hold the other widgets and add it to the right side of the PanedWindow
        self.right_frame = tk.Frame(self.frame)
        self.frame.add(self.right_frame)

        self.label = tk.Label(self.right_frame, text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n保存先のディレクトリを入力または選択してください。\n")
        self.label.pack()

        self.entry_frame = tk.Frame(self.right_frame)
        self.entry_frame.pack(fill=tk.X)
        self.entry = tk.Entry(self.entry_frame, bg='white')
        self.entry.insert(0, "Enter your directory path here")
        self.entry.config(fg="grey")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        if last_directory_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, last_directory_path)
            self.entry.config(fg="black")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.browse_button = tk.Button(self.entry_frame, command=self.browse_directory, borderwidth=0)
        self.browse_button.pack(side=tk.RIGHT)
        file_icon = tk.PhotoImage(file="assets/file_icon.png")
        file_icon = file_icon.subsample(30, 30)
        self.browse_button.config(image=file_icon)
        self.browse_button.image = file_icon

        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack(fill=tk.X)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.back_to_top_window)
        self.back_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_window)
        self.next_button.pack(side=tk.RIGHT)



    def _clear_placeholder(self, event):
        if self.entry.get() == "Enter your directory path here":
            self.entry.delete(0, "end")
            self.entry.config(fg = "black")


    def browse_directory(self):
        # Use the last selected directory path as the initial directory
        directory_path = filedialog.askdirectory(initialdir=self.entry.get())
        if directory_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, directory_path)

    def back_to_top_window(self):
        self.back_callback()

    def next_window(self):
        directory_path = self.entry.get()
        if directory_path:
            self.next_callback(directory_path)
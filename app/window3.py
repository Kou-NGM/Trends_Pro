# File: window3
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

class ThirdWindow:
    def __init__(self, root, back_callback, word, total_posts, next_window_callback):
        self.root = root
        self.frame = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.back_callback = back_callback

        # Load the image and resize it to fit the window
        image = Image.open("assets/image2.JPG")
        image = image.resize((int(root.winfo_screenwidth()//3), int(root.winfo_screenheight()*0.8)), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Create a label to hold the image and add it to the left side of the PanedWindow
        image_label = tk.Label(self.frame, image=image)
        image_label.image = image
        self.frame.add(image_label)

        # Create a frame to hold the other widgets and add it to the right side of the PanedWindow
        self.right_frame = tk.Frame(self.frame)
        self.frame.add(self.right_frame)

        self.current_word_var = tk.StringVar(value="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWord: loading...")
        self.total_posts_var = tk.IntVar(value=total_posts)
        self.word_label = tk.Label(self.right_frame, textvariable=self.current_word_var)
        self.word_label.pack()
        self.posts_label = tk.Label(self.right_frame, textvariable=self.total_posts_var)
        self.posts_label.pack()

        self.progress_bar = Progressbar(self.right_frame, length=200, mode='determinate')
        self.progress_bar.pack()

        self.complete_message_var = tk.StringVar(value="")
        self.complete_message_label = tk.Label(self.right_frame, textvariable=self.complete_message_var)
        self.complete_message_label.pack()

        self.next_button = tk.Button(self.right_frame, text="Next", command=next_window_callback)
        self.next_button.pack()
        self.next_button.pack_forget()  # Hide the button initially




    def back_to_second_window(self):
        self.back_callback()

    def update_status(self, current_word, progress, total_posts):
        self.current_word_var.set(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWord: {current_word}")
        self.total_posts_var.set("Total posts: {:,}".format(total_posts))
        self.update_progress(progress)
        if progress == 100:
            self.next_button.pack()  # Show the button when progress reaches 100%

    def update_progress(self, progress):  # 追加：プログレスバーの更新メソッド
        self.progress_bar['value'] = progress
        # 追加：プログレスが100%に達したら、完了メッセージを表示
        if progress >= 100:
            self.complete_message_var.set("完了しました。")

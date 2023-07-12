# File: window5
from urllib.parse import quote
import webbrowser
import time
import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd

class Window5:
    def __init__(self, root, result_path, back_callback):
        self.root = root
        self.frame = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.result_path = result_path
        self.back_callback = back_callback

        # Load the image and resize it to fit the window
        image = Image.open("assets/image3.JPG")
        image = image.resize((int(root.winfo_screenwidth()//3), int(root.winfo_screenheight()*0.8)), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Create a label to hold the image and add it to the left side of the PanedWindow
        image_label = tk.Label(self.frame, image=image)
        image_label.image = image
        self.frame.add(image_label)

        # Create a frame to hold the other widgets and add it to the right side of the PanedWindow
        self.right_frame = tk.Frame(self.frame)
        self.frame.add(self.right_frame)

        self.label = tk.Label(self.right_frame, text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.label.pack()
        self.back_button = tk.Button(self.right_frame, text="トップページに戻る", command=self.back_to_top_window)
        self.back_button.pack()

        self.search_option = tk.StringVar(value="top5")
        self.top5_radio = tk.Radiobutton(self.right_frame, text="上位５つをGoogleTrendsで検索", variable=self.search_option, value="top5")
        self.top5_radio.pack()
        self.all_radio = tk.Radiobutton(self.right_frame, text="全てをGoogleTrendsで検索", variable=self.search_option, value="all")
        self.all_radio.pack()

        self.selected_radio = tk.Radiobutton(self.right_frame, text="要素を選択してGoogleTrendsで検索", variable=self.search_option, value="selected", command=self.show_listbox)
        self.selected_radio.pack()

        self.listbox = tk.Listbox(self.right_frame, selectmode=tk.MULTIPLE)
        df = pd.read_csv(self.result_path)
        for word in df['word']:
            self.listbox.insert(tk.END, word)

        self.listbox.pack_forget()

        self.open_trends_button = tk.Button(self.right_frame, text="Open Google Trends", command=self.open_google_trends)
        self.open_trends_button.pack()


    def show_listbox(self):
        # Show the listbox when the "selected" radio button is clicked
        self.listbox.pack()

    def open_google_trends(self):
        # Read the csv file
        df = pd.read_csv(self.result_path)

        # Check the selected search option
        if self.search_option.get() == "top5":
            # Get the top 5 words
            words = df['word'].head(5).tolist()
        elif self.search_option.get() == "all":
            # Get all words
            words = df['word'].tolist()
        else:
            # Get selected words
            selected_indices = self.listbox.curselection()
            words = [self.listbox.get(i) for i in selected_indices]

        # Split the words into chunks of 5
        word_chunks = [words[i:i + 5] for i in range(0, len(words), 5)]

        # URL encode the words and join them with a comma, then open each chunk in a new window
        for chunk in word_chunks:
            encoded_words = [quote(word) for word in chunk]
            query = ','.join(encoded_words)
            url = f"https://trends.google.co.jp/trends/explore?geo=JP&q={query}"
            webbrowser.open_new(url)
            time.sleep(random.randint(1, 5))  # Wait for a random amount of time between 1 and 5 seconds

    def back_to_top_window(self):
        # Destroy the widgets
        self.frame.destroy()
        self.back_callback()

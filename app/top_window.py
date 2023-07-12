# File: top_window
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, simpledialog
import pandas as pd
from tkinter import ttk
from PIL import Image, ImageTk



class ListboxDialog(simpledialog.Dialog):
    def __init__(self, parent, title = None, list_items=None):
        self.list_items = list(list_items) if list_items is not None else []
        super().__init__(parent, title=title)

    def body(self, master):
        self.listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill="both", expand=True)
        for item in self.list_items:
            self.listbox.insert("end", item)
        return self.listbox

    def apply(self):
        try:
            selected_indices = self.listbox.curselection()
            self.result = [self.listbox.get(i) for i in selected_indices]
        except IndexError:
            self.result = None





class TopWindow:

    def __init__(self, root, callback, google_trends_callback):
        self.frame = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.callback = callback

        # Load the image and resize it to fit the window
        image = Image.open("assets/image0.JPG")
        image = image.resize((int(root.winfo_screenwidth()//3), int(root.winfo_screenheight()*0.8)), Image.LANCZOS)  # resize image to half of screen width and full screen height
        image = ImageTk.PhotoImage(image)  # convert PIL Image object to Tkinter PhotoImage object

        # Create a label to hold the image and add it to the left side of the PanedWindow
        image_label = tk.Label(self.frame, image=image)
        image_label.image = image  # keep a reference to the image object
        self.frame.add(image_label)

        # Create a frame to hold the other widgets and add it to the right side of the PanedWindow
        self.right_frame = tk.Frame(self.frame)
        self.frame.add(self.right_frame)

        # Add a label at the top of the frame
        self.label = tk.Label(self.right_frame, text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n調べたい単語を入力して下さい。複数ある場合は,で区切って下さい。\nまた、調べたい単語のリストを含むcsvファイルを参照することもできます。\n")
        self.label.pack()

        # Add a checkbox for GoogleTrends CSV file
        self.is_google_trends_csv = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.right_frame, text="GoogleTrendsのCSVファイル", variable=self.is_google_trends_csv)
        self.checkbox.pack()

        # Create a new frame to hold the entry widget and the browse button
        self.entry_frame = tk.Frame(self.right_frame)
        self.entry_frame.pack(fill=tk.X)  # fill the X direction to match the parent's width

        self.entry = tk.Entry(self.entry_frame, bg='white')
        self.entry.insert(0, "Enter your words here")
        self.entry.config(fg="grey")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)  # pack to the left and fill the remaining space in the entry_frame

        self.browse_button = tk.Button(self.entry_frame, command=self.browse_file, borderwidth=0)  # set borderwidth to 0
        self.browse_button.pack(side=tk.RIGHT)  # pack to the right of the entry in the entry_frame
        # Load the file icon and set it as the button image
        file_icon = tk.PhotoImage(file="assets/file_icon.png")  # replace with the path to your file icon
        file_icon = file_icon.subsample(30, 30)  # reduce the image size by half
        self.browse_button.config(image=file_icon)
        self.browse_button.image = file_icon  # keep a reference to the image object

        # Create a new frame to hold the buttons
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack()

        self.google_trends_button = tk.Button(self.button_frame, text="Google Trends検索を行う", command=self.google_trends)
        self.google_trends_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_window)
        self.next_button.pack(side=tk.RIGHT)

        self.google_trends_callback = google_trends_callback

        self.words = None

        self.error_label = tk.Label(self.right_frame, text="", fg="red")
        self.error_label.pack()





    def _clear_placeholder(self, event):
        if self.entry.get() == "Enter your words here":
            self.entry.delete(0, "end")
            self.entry.config(fg = "black")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            if self.is_google_trends_csv.get():  # If the checkbox is checked
                df = pd.read_csv(file_path, skiprows=2, usecols=[0],
                                 header=None)  # Skip the first 2 rows and read only the first column
                # Use ListboxDialog to let the user select multiple items
                selected_items = ListboxDialog(self.frame, title="Select items", list_items=df[0].tolist()).result
                if selected_items:
                    self.words = [word.replace(' ', '').replace('　', '') for word in selected_items]
            else:
                df = pd.read_csv(file_path, header=None)
                if messagebox.askyesno("Confirm", "Does the file have column names?"):
                    df.columns = df.iloc[0]
                    df = df[1:]
                    col_name = ListboxDialog(self.frame, title="Select a column", list_items=df.columns).result
                    if isinstance(col_name, list):
                        col_name = col_name[0]
                    self.words = [word.replace(' ', '').replace('　', '') for word in df[col_name].tolist()]


                else:
                    self.words = [word.replace(' ', '').replace('　', '') for word in df[0].tolist()]

    def next_window(self):
        if not self.words:  # ファイル参照がされていなければ、入力欄から読み込む
            self.words = [word.replace(' ', '').replace('　', '') for word in self.entry.get().split(',')]
        if self.words:
            self.callback(self.words)


    def google_trends(self):
        if not self.words:  # ファイル参照がされていなければ、入力欄から読み込む
            # Remove all spaces (including full-width spaces) from each word
            self.words = [word.replace(' ', '').replace('　', '') for word in self.entry.get().split(',')]
        if not self.words:
            self.error_label.config(text="調べたい単語を入力して下さい")
        else:
            self.error_label.config(text="")  # Clear the error message
            self.google_trends_callback(self.words)

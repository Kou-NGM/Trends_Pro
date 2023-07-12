# File: window4
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # new import
import pandas as pd  # new import
import matplotlib.pyplot as plt  # new import
import matplotlib.colors as mcolors  # new import
from app.window5 import Window5  # Add this line
import webbrowser  # new import

class FourthWindow:
    def __init__(self, root, total_posts, sorted_results_path, instagram_search, back_callback):
        self.root = root
        self.frame = tk.Frame(root)  # Ensure self.frame is defined before creating the back_button
        self.frame.pack(side=tk.BOTTOM) #無理やり下に表示 #, anchor=tk.SW
        self.total_posts_label = tk.Label(self.root, text=f'Total posts: {total_posts:,}')  # Display total_posts
        self.total_posts_label.pack()
        self.sorted_results_path = sorted_results_path  # Add this line
        self.back_to_top_window = back_callback  # Add this line

        # Add bar chart
        # Read the sorted results directly
        df_results = pd.read_csv(sorted_results_path)
        tableau_colors = list(mcolors.TABLEAU_COLORS)
        bar_colors = [tableau_colors[i%len(tableau_colors)] for i in range(len(df_results['word']))]
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(df_results['word'], df_results['posts_count'], color=bar_colors)
        ax.set_xlabel('Word')
        ax.set_ylabel('Posts Count')
        ax.set_title('Number of posts count for each word')
        plt.xticks(rotation=45)
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: instagram_search.human_format(x)))
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', ha='center', va='bottom')
        fig.tight_layout()

        # Create tkinter canvas with matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master=root)  # Use self.canvas instead of canvas
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.NONE, expand=1)


        back_button = tk.Button(self.frame, text='トップページに戻る', command=back_callback)  # use back_callback here
        back_button.pack()


        # Save back_callback as an instance variable
        self.back_callback = back_callback


        # Add a button to go to Window5
        self.go_to_window5_button = tk.Button(self.frame, text='GoogleTrendsで検索', command=self.go_to_window5)
        self.go_to_window5_button.pack(side=tk.RIGHT)



    def destroy(self):
        # Destroy the widgets
        self.total_posts_label.destroy()
        self.canvas.get_tk_widget().destroy()  # Destroy the canvas widget
        self.frame.destroy()

    def go_to_window5(self):
        # Destroy current window
        self.destroy()
        self.window5 = Window5(self.root, self.sorted_results_path, self.back_to_top_window)  # Pass sorted_results_path and back_to_top_window



'''
Tkinterのpack()メソッドはウィジェットを配置するためのもので、以下のようないくつかのオプションを持っています：

side：ウィジェットが親ウィジェットに対してどの側に配置されるかを指定します。これにはTOP、BOTTOM、LEFT、RIGHTの4つの値があります。side=tk.TOPはウィジェットが親ウィジェットの上部に配置されることを意味します。

fill：ウィジェットが親ウィジェットのどの部分を占めるかを指定します。NONE（デフォルト）、X（水平方向）、Y（垂直方向）、BOTH（水平と垂直の両方）の4つの値があります。例えば、fill=tk.BOTHはウィジェットが親ウィジェットの可能な限り多くの空間を占めることを意味します。

expand：これは真偽値を取り、ウィジェットが親ウィジェットが大きくなるときにその空間を占めるかどうかを制御します。expand=1またはexpand=Trueは、親ウィジェットが拡大されたときにウィジェットがその追加のスペースを占めることを意味します。それに対してexpand=0またはexpand=Falseは、親ウィジェットが大きくなったときにウィジェットのサイズが変わらないことを意味します。
'''
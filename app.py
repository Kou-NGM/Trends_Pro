# File: app
import tkinter as tk
from app.top_window import TopWindow
from app.window2 import SecondWindow
from app.window3 import ThirdWindow
from app.window4 import FourthWindow
from app.window5 import Window5  # new import
from app.logi import InstagramHashtagSearch, BrowserDriver
import threading  # new import
import os
import pandas as pd
import subprocess
import sys
import os


class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1024x768')
        self.top_window = None
        self.second_window = None
        self.third_window = None
        self.words = None
        self.output_directory = os.getcwd()
        self.browser_driver = BrowserDriver()  # create BrowserDriver instance here
        self.instagram_search = InstagramHashtagSearch(self.browser_driver, update_callback=self.update_status)
        self.last_directory_path = ""  # Add this line to store the last selected directory path

        # Set up handler for window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.window5 = None



    def update_status(self, status):
        """
        Updates the application status with the provided status message.

        This is a dummy implementation and should be replaced with code that
        updates the application's GUI with the new status.
        """
        print(status)




    def get_base_dir(self):  # add 'self' here
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def on_window_close(self):
        # Close Selenium browser when window is closed
        self.browser_driver.driver.quit()
        # Run the kill_chrome.py script
        script_path = os.path.join(self.get_base_dir(), "For_Dev", "kill_chrome.py")  # use 'self.' here
        subprocess.run(["python", script_path])
        # Then destroy the window
        self.root.destroy()


    def create_top_window(self):
        if self.second_window:
            self.second_window.frame.destroy()
        self.top_window = TopWindow(self.root, self.next_window, self.create_window5)

    def create_second_window(self):
        if self.top_window:
            self.top_window.frame.destroy()
        self.second_window = SecondWindow(self.root, self.back_window, self.run_instagram_search, self.last_directory_path)

    def next_window(self, words):
        self.words = words
        self.create_second_window()

    def back_window(self):
        self.create_top_window()

    def create_third_window(self):
        if self.second_window:
            self.second_window.frame.destroy()
        total_posts = self.instagram_search.total_posts if self.instagram_search else 0
        self.third_window = ThirdWindow(self.root, self.back_window, self.words, total_posts, self.create_fourth_window)


    def run_instagram_search(self, output_directory):
        self.last_directory_path = output_directory  # Update the last directory path here
        self.output_directory = output_directory
        self.instagram_search.words = self.words  # New line
        self.instagram_search.output_directory = output_directory  # New line
        self.create_third_window()
        # Reset the display of ThirdWindow before starting a new search
        self.third_window.update_status("loading...", 0, 0)
        self.instagram_search = InstagramHashtagSearch(self.browser_driver, self.words, self.output_directory, self.third_window.update_status)

        # Start the Instagram search in a new thread
        threading.Thread(target=self.execute_instagram_search).start()


    def execute_instagram_search(self):
        self.instagram_search.fetch_post_counts()
        self.instagram_search.print_results()
        self.instagram_search.save_results_to_csv()
        self.instagram_search.sort_results()
        self.instagram_search.plot_and_save_bar_chart()
        self.instagram_search.save_sorted_results_in_different_formats()


    def create_fourth_window(self):
        if self.third_window:
            self.third_window.frame.destroy()
        sorted_results_path = self.instagram_search.sort_results()  # get the path of the sorted results
        self.fourth_window = FourthWindow(self.root, self.instagram_search.total_posts, sorted_results_path, self.instagram_search, self.back_to_top_window)  # Pass sorted_results_path here


    def back_to_top_window(self):
        if hasattr(self, 'fourth_window') and self.fourth_window:
            self.fourth_window.destroy()
        if hasattr(self, 'window5') and self.window5:
            self.window5.frame.destroy()
        self.create_top_window()

    def create_window5(self, words):
        if self.top_window:
            self.top_window.frame.destroy()
        # Convert the list of words to a DataFrame and save it to a csv file
        df = pd.DataFrame(words, columns=["word"])
        result_path = os.path.join(self.output_directory, "words.csv")
        df.to_csv(result_path, index=False)
        self.window5 = Window5(self.root, result_path, self.back_to_top_window)


def main():
    root = tk.Tk()
    root.title("Trends_Pro")  # ウィンドウの名前を設定
    app = Application(root)
    app.create_top_window()
    root.mainloop()


if __name__ == "__main__":
    main()

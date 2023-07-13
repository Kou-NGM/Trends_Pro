# File: logi.py
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib
import sys
from matplotlib import font_manager
import matplotlib.colors as mcolors
import datetime
import openpyxl

from selenium.webdriver.common.service import Service


class BrowserDriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--lang=en')

        chrome_driver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "driver", "chromedriver.exe")
        selenium_version = tuple(int(num) for num in selenium.__version__.split('.')[:2])

        if selenium_version >= (4, 0):
            webdriver_service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(service=webdriver_service, options=options)
        else:
            self.driver = webdriver.Chrome(chrome_driver_path, options=options)


class InstagramHashtagSearch:
    def __init__(self, browser_driver, words=None, output_directory=None, update_callback=None):
        self.browser_driver = browser_driver
        self.driver = self.browser_driver.driver
        self.update_callback = update_callback
        self.check_font_availability()

        self.base_url = 'https://www.instagram.com/explore/tags/'
        self.words = words
        self.output_directory = output_directory
        self.results_directory = None  # Add this line
        self.results = []
        self.total_posts = 0
        # Add a timestamp attribute
        self.timestamp = self.get_timestamp()


    @staticmethod
    def check_font_availability():
        fonts = [f.name for f in font_manager.fontManager.ttflist]
        available_fonts = ['Meiryo', 'MS Gothic', 'MS Mincho', 'Takao']

        for font in available_fonts:
            if font in fonts:
                matplotlib.rcParams['font.family'] = font
                break
        else:
            continue_program = input("日本語フォントが見つからない場合でもプログラムを続行しますか？ (y/n): ")
            if continue_program.lower() != 'y':
                sys.exit("プログラムを終了します。")


    # Define helper functions
    @staticmethod
    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.1f%s' % (num, ['', 'K', 'M', 'B'][magnitude])

    @staticmethod
    def get_timestamp():
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        return timestamp



    def fetch_post_counts(self):
        # Reset results and total_posts at the beginning of each search
        self.results = []
        self.total_posts = 0

        # Create a directory for the results
        first_word = self.words[0] if self.words else "unknown"
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        self.results_directory = os.path.join(self.output_directory, f'{first_word}_Insta_Trends_{timestamp}')
        os.makedirs(self.results_directory, exist_ok=True)

        for i, word in enumerate(self.words):
            url = self.base_url + word.strip() + '/'
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
            match = re.search(r'([\d.,]+[KMB]?)\s*posts', self.driver.page_source, re.IGNORECASE)

            if match:
                posts_count_str = match.group(1).replace(',', '')
                if 'K' in posts_count_str:
                    posts_count = int(float(posts_count_str.replace('K', '')) * 1000)
                elif 'M' in posts_count_str:
                    posts_count = int(float(posts_count_str.replace('M', '')) * 1000000)
                elif 'B' in posts_count_str:
                    posts_count = int(float(posts_count_str.replace('B', '')) * 1000000000)
                else:
                    posts_count = int(float(posts_count_str))
                self.total_posts += posts_count
                self.results.append([word, posts_count])
            else:
                self.results.append([word, 0])

            time.sleep(random.randint(1, 3))
            self.current_word = word
            self.progress = (i + 1) / len(self.words) * 100
            self.update_status()






    def update_status(self):
        if self.update_callback:
            self.update_callback(self.current_word, self.progress, self.total_posts)




    def print_results(self):
        for result in self.results:
            print(f"Word: {result[0]}, Post count: {result[1]}")

        print(f"Total posts count: {self.total_posts}")

    def save_results_to_csv(self):
        df = pd.DataFrame(self.results, columns=['word', 'posts_count'])
        df.to_csv(os.path.join(self.results_directory, 'results.csv'), index=False, encoding='utf-8')

    def sort_results(self):
        df_results = pd.read_csv(os.path.join(self.results_directory, 'results.csv'))
        df_results = df_results.dropna(subset=['posts_count'])
        df_results['posts_count'] = df_results['posts_count'].astype(int)
        df_results = df_results.sort_values(by='posts_count', ascending=False)
        sorted_results_path = os.path.join(self.results_directory, 'sorted_results.csv')
        df_results.to_csv(sorted_results_path, index=False, encoding='utf-8-sig')
        return sorted_results_path  # return the path of the sorted results

    def save_sorted_results_in_different_formats(self):
        # Read the sorted results
        df_results = pd.read_csv(os.path.join(self.results_directory, 'sorted_results.csv'))

        # Save as a CSV file with "cp932" encoding
        df_results.to_csv(os.path.join(self.results_directory, 'sorted_results_jp.csv'), index=False, encoding='cp932')

        # Save as an Excel file
        df_results.to_excel(os.path.join(self.results_directory, 'sorted_results.xlsx'), index=False)

    def plot_and_save_bar_chart(self):
        # Read sorted results using the saved timestamp
        sorted_results_path = os.path.join(self.results_directory, 'sorted_results.csv')
        df_results = pd.read_csv(sorted_results_path)

        # Plot and save bar chart
        tableau_colors = list(mcolors.TABLEAU_COLORS)
        bar_colors = [tableau_colors[i%len(tableau_colors)] for i in range(len(df_results['word']))]
        plt.figure(figsize=(10, 5))
        bars = plt.bar(df_results['word'], df_results['posts_count'], color=bar_colors)
        plt.xlabel('Word')
        plt.ylabel('Posts Count')
        plt.title('Number of posts count for each word')
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: self.human_format(x)))
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', ha='center', va='bottom')
        plt.tight_layout()
        # Save the chart using the saved timestamp
        chart_path = os.path.join(self.results_directory, 'bar_chart.png')
        plt.savefig(chart_path)
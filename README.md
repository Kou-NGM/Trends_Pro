# Trends_Pro

## 概要
Trends_Proは、Instagramのハッシュタグ検索を自動化し、結果を可視化するPythonアプリケーションです。ユーザーが指定したハッシュタグの投稿数を取得し、結果をCSVファイルとして保存します。また、結果を棒グラフとして可視化し、画像として保存します。入力した単語はGoogle Trends分析にてシームレスに分析することが可能です。


## 環境設定・インストール（Setting Up Your Environment）
まず最初に、このプロジェクトを実行するためにはPythonが必要です。Pythonは公式ウェブサイトからダウンロード可能です。このプロジェクトはPython 3.7以上で動作します。

ファイルを解凍後はコマンドプロンプト(Windows)やターミナル(Mac)を開き`cd`コマンドで解凍したファイルのパスに移動します。
```
cd /*解凍したファイルのパス*/
```

次にPythonのパッケージマネージャであるpipを使用して、必要なPythonライブラリをインストールする必要があります。以下のコマンドを使用してライブラリをインストールできます。以下の動作が必要なのは初回時のみで２回目に実行するときは必要ありません!!

Firstly, you will need Python to run this project. You can download Python from the official website. This project works with Python 3.7 and above.

Next, you'll need to install the necessary Python libraries using pip, which is Python's package manager. You can install the libraries using the following command:

```
 pip install selenium webdriver_manager pandas matplotlib openpyxl pillow
```




## 実行（Running the Program）
必要なソフトウェアとライブラリがインストールされていることを確認したら、以下のステップでプロジェクトをセットアップします：

1. このリポジトリをクローンまたはダウンロードします。
2. ターミナルを開き、リポジトリのディレクトリに移動します。
3. `python app.py` を実行して、スクリプトを起動します。

You can run the program from the command line as follows:

```
python app.py
```

## 使用方法
1. `app.py`を実行します。これにより、アプリケーションのGUIが開きます。
2. GUIを使用して、検索したいハッシュタグを入力します。
3. 「検索」ボタンをクリックします。アプリケーションはInstagramのハッシュタグ検索を自動的に実行し、結果をCSVファイルとして保存します。
4. 「結果を表示」ボタンをクリックすると、結果の棒グラフが表示されます。

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。

## 連絡先
質問やフィードバックがある場合は、GitHubの「Issues」タブを使用してください。

---

# Trends_Pro

## Overview
Trends_Pro is a Python application that automates Instagram hashtag searches and visualizes the results. It fetches the number of posts for user-specified hashtags and saves the results as a CSV file. It also visualizes the results as a bar chart and saves it as an image.The entered words can be seamlessly analyzed by Google Trends analysis.

## Installation
1. Clone or download this repository.
2. Install the necessary Python packages. These include `tkinter`, `selenium`, `pandas`, `matplotlib`, and others.
3. Download ChromeDriver and add it to your system path.

## Usage
1. Run `app.py`. This will open the application's GUI.
2. Use the GUI to enter the hashtags you want to search for.
3. Click the 'Search' button. The application will automatically perform Instagram hashtag searches and save the results as a CSV file.
4. Click the 'Show Results' button to display a bar chart of the results.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or feedback, please use the 'Issues' tab on GitHub.

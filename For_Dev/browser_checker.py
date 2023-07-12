# File: browser_checker
import psutil

def check_selenium_browser():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'] or 'firefox' in proc.info['name']:
            print(f"Selenium browser process found: PID={proc.info['pid']}, name={proc.info['name']}")

check_selenium_browser()

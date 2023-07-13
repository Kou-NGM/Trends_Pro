# File: kill_chrome
import os
import signal
import subprocess

def kill_chrome_driver():
    if os.name == 'nt':  # For Windows
        os.system('taskkill /f /im chromedriver.exe /T >nul 2>&1')
    else:  # For Linux and Mac
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if b'chromedriver' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

kill_chrome_driver()

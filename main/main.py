from dotenv import load_dotenv
import os

from sys import platform
if platform == "linux" or platform == "linux2":
    from linux_win import *
elif platform == "win32":
    from windows import *

load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    main_window(api_key)

if __name__ == '__main__':
    main()
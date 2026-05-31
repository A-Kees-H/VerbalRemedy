from listen_utils.hotkeys import setup_hotkeys
from setproctitle import setproctitle
import sys
from datetime import datetime
import keyboard 

if __name__ == "__main__":
    setup_hotkeys()
    print("Hold AltGr to transcribe and print. Hold Numlock to Do a Command...")
    keyboard.wait()
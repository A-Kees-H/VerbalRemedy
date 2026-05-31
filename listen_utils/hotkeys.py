import keyboard
import pyautogui
from listen_utils.audio import start_recording, stop_recording
from listen_utils.whisper_utils import transcribe_file
from listen_utils.american_to_british import american_to_british
from listen_utils.command_functions import runner, switch_or_load, powershell_runner, get_llm_response
from reminder_windows import advisory

# Tracks recording state and active handler
recording_flag = False
current_handler = None  

def handle_transcription_altgr(text):
    pyautogui.typewrite(text, interval=0.001)

def handle_transcription_shift_numlock(text):
    response = get_llm_response(text)
    advisory(response)

def handle_transcription_numlock(text):
    text = text.replace(".", "")
    print(text)
    if text in ["qb", "run qb", "run cubey", "run cube", "run tv", "run q b", "run cue bee", "thank you, being", "from a cubie", "remembering", "right here, please", "weren't you big?", "run to qb"]:
        switch_or_load("qbittorrent", "C:/Program Files/qBittorrent/qbittorrent.exe")
    elif text in ["open videos", "videos"]:
        powershell_runner("C:/Users/Kees/Work/Projects/voice_recognition/VideoTime.lnk")
    elif text in ["run brave", "brave"]:
        runner("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
    elif text in ["vs code", "run vs code"]:
        runner("C:/Users/Kees/AppData/Local/Programs/Microsoft VS Code/Code.exe")
    elif text in ["run powershell", "powershell"]:
        powershell_runner("C:/Windows/System32/schtasks.exe /run /tn 'NoUACPowershell'")
    elif text in ["sublime", "run sublime"]:
        switch_or_load("sublime", "C:/Program Files/Sublime Text/sublime_text.exe")
    elif text in ["firefox", "run firefox"]:
        switch_or_load("firefox", "C:/Program Files/Mozilla Firefox/firefox.exe")
    elif len(text.split(" ")) > 3:
        response = get_llm_response(text)
        advisory(response, 60)
    else:
        advisory("No executable audio", 3)

def clean_up_text(text):
    if text.endswith("."):
        text = text[:-1]
    if not text or text == "[blank_audio]":
        print("no words detected")
        return ""
    return american_to_british(text)

# Start recording for push-to-talk, but only sets the handler
def start_push_to_talk(handler):
    global recording_flag, current_handler
    if not recording_flag:
        current_handler = handler
        start_recording()
        recording_flag = True

# Stop recording and process audio; attached once
def stop_and_process(event):
    global recording_flag, current_handler
    if recording_flag:
        wav_file = stop_recording()
        recording_flag = False
        text = transcribe_file(wav_file)
        text = clean_up_text(text.lower())
        if text and current_handler:
            current_handler(text)
        current_handler = None

# Attach the release listener **once**
keyboard.on_release(stop_and_process, suppress=False)

# Setup all hotkeys
def setup_hotkeys():
    keyboard.add_hotkey("alt gr", lambda: start_push_to_talk(handle_transcription_altgr))
    keyboard.add_hotkey("numlock", lambda: start_push_to_talk(handle_transcription_numlock))
    keyboard.add_hotkey("shift+numlock", lambda: start_push_to_talk(handle_transcription_shift_numlock))

setup_hotkeys()
from llm_client import LLMController, GetUser
from datime import get_current_date
import os
import subprocess
import win32gui
import win32con
import time

def focus_window_by_title(partial_title: str):
    try:
        target_hwnd = None

        def enum_handler(hwnd, _):
            nonlocal target_hwnd
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = win32gui.GetWindowText(hwnd)
            if partial_title.lower() in title.lower():
                target_hwnd = hwnd

        win32gui.EnumWindows(enum_handler, None)
        if not target_hwnd:
            raise RuntimeError("Window not found")

        # Option 1: just bring to front, don't touch size/state
        win32gui.SetForegroundWindow(target_hwnd)

        # If that fails when minimized, comment the line above and try this:
        # win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)
        # win32gui.SetForegroundWindow(target_hwnd)

        return True

    except RuntimeError:
        print(f"{partial_title} not open")
        return False

def open_timebox_schedule():
    timebox_folder_path = "C:/Users/Kees/Work/Projects/central_planning/daily_plans/"
    def get_timebox_filename():
        return get_current_date() + "_timebox.txt"

    timebox_path = os.path.join(timebox_folder_path, get_timebox_filename())
    try:
        with open(timebox) as f:
            pass
    except:
        print("today's timebox schedule not found")

def runner(program_path, parameters=[]):
    run_command = [program_path] + parameters
    print(run_command)
    run = subprocess.run(
        run_command, 
        cwd="C:/Program Files/OneCommander",
        capture_output=True,
        text=True
    )

def powershell_runner(command):
    """
    Runs a PowerShell command without showing the PowerShell window.
    """
    subprocess.run(
        [
            "powershell.exe",
            "-Command",
            command
        ],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def get_llm_response(text):

    system_prompt = ""

    model_names = ["gpt-5.1", "gpt-4.1-nano", "gpt-3.5-turbo"]
    model = model_names[0]  # or [1] if you want gpt-3.5
    key = GetUser().api_key
    llm = LLMController(system_prompt=system_prompt, model=model, api_key=key)
    output = llm.respond(text)

    return output

def switch_or_load(app, exe_path):
    if not focus_window_by_title(app):
        runner(exe_path)

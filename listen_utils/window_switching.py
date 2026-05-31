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

if __name__ == "__main__":
    # examples: call these when your backend event happens
    focus_window_by_title("Mozilla Firefox")
    time.sleep(0.5)
    focus_window_by_title("Sublime Text")
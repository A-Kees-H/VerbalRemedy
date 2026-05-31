import subprocess
import os

# Set paths relative to this module
WHISPER_DIR = open("path_to_your_whisper_cli_exe.txt")
WHISPER_EXE = os.path.join(WHISPER_DIR, "whisper-cli.exe")
MODEL = os.path.join(WHISPER_DIR, "ggml-tiny.en.bin")

def transcribe_file(filename):
    """
    Run whisper-cli.exe on the given WAV file and return the transcription text.
    Prints full stdout and stderr for debugging.
    Prevents a CMD window from appearing when calling the subprocess on Windows.
    """
    # Use startupinfo to prevent cmd window on Windows
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    result = subprocess.run(
        [WHISPER_EXE, "-m", MODEL, "-f", filename, "-nt"],
        capture_output=True,
        text=True,
        startupinfo=startupinfo
    )

    # Print full output for debugging
    """print("--- Whisper Output ---")
    print(result.stdout.strip())
    if result.stderr.strip():
        print("--- Whisper STDERR ---")
        print(result.stderr.strip())
    print("---------------------")"""

    return result.stdout.strip()

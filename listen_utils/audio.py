import sounddevice as sd
import numpy as np
import wave
import os
import tempfile
from datetime import datetime
import winsound

SAMPLE_RATE = 16000
PLAYBACK_ENABLED = True
SAVE_RECORDINGS = True  # <-- toggle this
MIC_DEVICE_INDEX = 5  # Replace with your mic's device index

# Setup recordings directory only if saving is enabled
if SAVE_RECORDINGS:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RECORDINGS_DIR = os.path.join(BASE_DIR, "../voice_recordings")
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

recording = False
audio_frames = []
stream = None

def audio_callback(indata, frames, time, status):
    global audio_frames
    audio_frames.append(indata.copy())

def start_recording():
    global recording, audio_frames, stream
    audio_frames = []
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        device=MIC_DEVICE_INDEX
    )
    stream.start()
    recording = True
    print("Recording...")

def stop_recording():
    global recording, stream
    if not recording:
        return None

    stream.stop()
    recording = False
    print("Processing...")

    if not audio_frames:
        print("No audio captured, skipping transcription.")
        return None

    audio = np.concatenate(audio_frames, axis=0)

    # Decide where to save
    if SAVE_RECORDINGS:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.wav")
    else:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = temp_file.name
        temp_file.close()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())

    if PLAYBACK_ENABLED:
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Error playing audio: {e}")

    if SAVE_RECORDINGS:
        print(f"Saved to: {filename}")

    return filename
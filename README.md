# VerbalRemedy
### A featherweight voice-to-text-to-LLM Python implementation for Whisper models

To make this work, you'll need to download a Whisper voice to text model from here: https://github.com/ggml-org/whisper.cpp
And then convert it to an executable called whisper-cli.exe. Instructions in link. This is a bit messy and will requiring using cmake to build an executable, but you're on Github, I trust you to handle that

Put the folder path of that executable in listen_utils/path_to_your_whisper_cli_exe.txt and you should be good to go

If you want this to run all the time, pop a shortcut to listen.pyw to your startup folder (C:\{YOUR USER DIR}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup)

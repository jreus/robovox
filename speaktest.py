"""
TTS Engine Tests

(c) 2022 Jonathan Reus

pyttsx3 docs at: https://pyttsx3.readthedocs.io/en/latest/
"""

import pyttsx3
import sys, os

import os

from pyaudio import PyAudio


class silence_stdout:
    """
    PyAudio is noisy af every time you initialise it, which makes reading the
    log output rather difficult.  The output is being made by the
    C internals, Therefore the nuclear option was selected: swallow all stderr
    and stdout for the duration of PyAudio's use.

    Lifted and adapted from StackOverflow:
      https://stackoverflow.com/questions/11130156/
    """
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self) -> None:
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)
        return None

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

tts = pyttsx3.init('espeak')
voices = tts.getProperty('voices')

def print_voices(voices):
    print(f"Voices:")
    for voice in voices:
        print(f"\t{voice}")

text = "I will say this with my voicececece."
tts.say(text)
tts.runAndWait()
#tts.stop()

rate = tts.getProperty('rate')
vol = tts.getProperty('volume')
pitch = tts.getProperty('pitch')
print(f"Rate:{rate}\nVolume:{vol}\nPitch:{pitch}")

tts.setProperty('rate', 100)
tts.setProperty('volume', 0.6)
tts.setProperty('pitch', 25)


# Save to file
filepath = 'HelloWorld.wav'
res = tts.save_to_file(text, filepath)
print(res)
tts.runAndWait()
tts.stop()

# Using sounddevice (requires more work to play back 22050 files generated by espeak)
# import sounddevice as sd
# import soundfile as sf
# import numpy as np
# #data, sr = sf.read(filepath, dtype='float32')
# data, sr = sf.read(filepath, dtype='int16')
# #data, sr = sf.read(filepath)
# print(f"Opened File:{filepath}, sr:{sr}, data:{len(data)}, shape:{data.shape}")
# systemsr = 48000
# sd.play(data, blocking=True)
# status = sd.wait()

# Using pydub, higher level interface build on top of pyaudio/portaudio
import pydub
from pydub.playback import play
wav = pydub.AudioSegment.from_file(filepath, format="wav")
# pyaudio is very verbose and might spit out some errors: see:
#   https://stackoverflow.com/questions/37733318/pyaudio-warnings-poluting-output
#   https://stackoverflow.com/questions/67765911/how-do-i-silence-pyaudios-noisy-output
with silence_stdout() as dummy:
    play(wav)

#os.system('cmd /c "stty echo"')
sys.exit(1)

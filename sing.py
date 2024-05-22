import sounddevice as sd
import numpy as np

# Samples per second
SAMPLING_FREQUENCY = 44100

# Base note frequencies
freq = {"C4": 261.6256, "D4": 293.6648, "E4": 329.6276, "F4": 349.2282, "G4":391.9954 , "A4": 440.0000, "B4": 493.8833}

def _pitch(note, duration, Fs=SAMPLING_FREQUENCY):
    """Produce sine wave that corresponds to given note and duration"""

    # Multiply the amount of samples per second by the duration 
    # and Normalize time such that "Every 1/Fs seconds the next number is read"
    t = np.arange(duration * Fs) / Fs
    # Recall simple Harmonic motion sin(wt) where angular frequency(w) = 2*pi*f
    # sin(wt) = sin(2*pi*note_frequency*t)
    f = _adjust_note_frequency(note)
    y = np.sin(2 * np.pi * t * f)
    # 
    for i in range(2,131072, 1024):
        # y += pow(2, -i) *  np.sin(2 * np.pi * f * (i) * t)
        # if i % 2:  
        y += pow(2, -i) *  np.sin(2 * np.pi * f / (i+1) * t)  

    return y * 0.5

def _adjust_note_frequency(note):
    """Adjust notes based on 4th octave notes"""
    name,octave = note[0], int(note[1])
    return freq[name + '4'] * pow(2, octave - 4)


def _riff(notes, Fs=SAMPLING_FREQUENCY):
    """Convert standard pitch notes and durations into list of waves"""
    # return wave
    return np.array([_pitch(note, duration, Fs) for note,duration in notes])

def sing(song, Fs=SAMPLING_FREQUENCY):
    """Play sequence of notes from standard pitch notation and duration data"""

    for riff in _riff(song, Fs):
        print(riff)
        sd.play(riff, Fs)
        sd.wait()

def main():
    song = zip(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"], [2]*8)
    sing(song)
  

if __name__ == "__main__":
    main()
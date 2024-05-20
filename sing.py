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
    return np.sin(2 * np.pi * t * freq[note])

def _riff(notes, Fs=SAMPLING_FREQUENCY):
    """Convert standard pitch notes and durations into list of waves"""
    # return wave
    return np.array([_pitch(x[0], x[1], Fs) for x in notes])

def sing(song, Fs=SAMPLING_FREQUENCY):
    """Play sequence of notes from standard pitch notation and duration data"""
    for riff in _riff(song, Fs):
        sd.play(riff, Fs)
        sd.wait()




def main():
    song = zip(["C4", "D4", "E4", "F4", "G4", "A4", "B4"], [0.5]*7)

    sing(song)


if __name__ == "__main__":
    main()
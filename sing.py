import sounddevice as sd
import numpy as np
# Samples per second
SAMPLING_FREQUENCY = 44100

funky_town_riff = [
    [('C5', 0.25), ('C3',0.25)], [('C5', 0.25), ('C4', 0.25)], [('A#4', 0.25),('C3',0.25)], [('C5', 0.5),('C4', 0.25), ('C3', 0.3)],  
    [('G4', 0.5),('C4',0.25), ('C3', 0.3)], [('G4', 0.25), ('C4', 0.25)], [('C5', 0.25), ('C3', 0.25)], [('F5', 0.25),('C4', 0.25)], 
    [('E5', 0.25),('C3', 0.25)], [('C5', 0.75), ('C4', 0.2)]
]

funky_town_melody = [
    ('C4', 0.5), ('C4', 0.25), ('C4', 0.25), ('E4', 0.5), ('E4', 0.25), ('E4', 0.3), ('G4', 0.4), ('G4', 0.4), ('E5', 0.4), ('S', 0.05), ('D4', 0.3), ('C5', 0.5)
]

funky_town_melody_two = [
    ('C5', 0.25), 
    [('D5', 0.25), ('F5', 0.25)],  [('D5', 0.25), ('F5', 0.25)], [('D5', 0.3), ('F5', 0.3)],  [('D5', 0.25), ('F5', 0.25)],   
    [('C5', 0.25), ('E5', 0.25)], [('C5', 0.25), ('E5', 0.25)], [('C5', 0.3), ('E5', 0.3)], [('C5', 0.25), ('E5', 0.25)],   
    [('B4', 0.25),('D5', 0.25)], [('B4', 0.25),('D5', 0.25)], [('B4', 0.3),('D5', 0.3)], [('B4', 0.25),('D5', 0.25)],  
    [('A4', 0.25), ('C5', 0.25)], [('A4', 0.25), ('C5', 0.25)],  [('A4', 0.3), ('C5', 0.3)], [('A4', 0.4), ('B4', 0.4)]
]

funky_town_melody_alt = [
    [('E4', 0.3),('D4', 0.3), ('B3', 0.3)], [('E4', 0.3),('D4', 0.3), ('B3', 0.3) ], [('E4', 0.3),('D4', 0.3), ('B3', 0.3) ], [('E4', 0.3),('D4', 0.3), ('B3', 0.3) ], 

]

funky_town_song = (funky_town_riff + [('S', 0.3)] + funky_town_riff + [('S', 0.4)] + funky_town_melody + funky_town_riff + 
                   funky_town_melody + funky_town_riff + funky_town_melody_two)

# Base note frequencies
freq = {"C4": 261.6256, "C#4": 277.1826, "D4": 293.6648, "D#4" : 311.1270, "E4": 329.6276, "F4": 349.2282, "F#4": 369.9944,"G4":391.9954 , "G#4": 415.3047, "A4": 440.0000, "A#4": 466.1638, "B4": 493.8833, "S": 0}

def _pitch(note, duration, Fs=SAMPLING_FREQUENCY, volume=0.3):
    """Produce sine wave that corresponds to given note and duration"""
    # Multiply the amount of samples per second by the duration 
    # and Normalize time such that "Every 1/Fs seconds the next number is read"
    t = np.arange(0, duration, 1/Fs)

    f = _adjust_note_frequency(note) if note != "S" else freq[note]
    y = np.sin(2 * np.pi * t * f)

    # Add overtones and undertones
    for i in range(2,17):
        y += pow(2, -i) *  np.sin(2 * np.pi * f * i * t)
        if not i % 2:  
            y += pow(2, -i) *  np.sin(2 * np.pi * f / i * t)  

    return apply_fade(y * volume)

def _adjust_note_frequency(note):
    """Adjust notes based on 4th octave notes"""
    name, octave = note[0],int(note[-1])
    if '#' in note:
        name += note[1]
    return freq[name + '4'] * pow(2, octave - 4)


def _riff(notes, Fs=SAMPLING_FREQUENCY):
    """Convert standard pitch notes and durations into list of waves"""
    riff = np.array([])
    for note in notes:
        if isinstance(note, list):
            riff = np.append(riff, _play_chord(note))
        else:
            note, duration = note
            riff = np.append(riff, _pitch(note, duration, Fs))
    return riff

def pad_arr(arr_one, arr_two):
    """combine different sized arrays"""
    padded_arr = None
    # Add smaller array to front of larger array
    if len(arr_one) < len(arr_two):
        arr_two[:len(arr_one)] += arr_one
        padded_arr = arr_two
    else:
        arr_one[:len(arr_two)] += arr_two
        padded_arr = arr_one
    
    return padded_arr

# adding arrs together will produce the sound of the notes playing together
def _play_chord(multiple_notes, Fs=SAMPLING_FREQUENCY):
    chord = None
    for note,duration in multiple_notes:
        if chord is None:
            chord = _pitch(note, duration, Fs)
        else:
            chord = pad_arr(chord,  _pitch(note, duration, Fs))

    return np.flip(chord) * 0.3

def apply_fade(wave, fade_duration=0.01, Fs=SAMPLING_FREQUENCY):
    """Apply a fade In & Out to a wave"""
    fade_samples = int(fade_duration * Fs)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    # Incrementally adjust amplitude per sample to achieve fade
    wave[:fade_samples] *= fade_in
    wave[-fade_samples:] *= fade_out
    return wave


def sing(song, Fs=SAMPLING_FREQUENCY):
    """Play sequence of notes from standard pitch notation and duration data"""

    # appending to arr makes a single track to play
    song_to_play = np.ndarray([])
    song_to_play = np.append(song_to_play, _riff(song,Fs))
    sd.play(song_to_play, Fs)
    sd.wait()

def main():
    sing(funky_town_song)
   
if __name__ == "__main__":
    main()
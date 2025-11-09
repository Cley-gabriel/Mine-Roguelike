import os, wave, struct, math

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SOUNDS_DIR = os.path.join(BASE, 'sounds')
MUSIC_DIR = os.path.join(BASE, 'music')
os.makedirs(SOUNDS_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)


def write_tone(path, seconds, freq, vol=0.5, sr=22050):
    if os.path.exists(path):
        return  # do not overwrite user assets
    n = int(seconds * sr)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        for i in range(n):
            t = i / sr
            s = math.sin(2 * math.pi * freq * t)
            val = int(max(-1.0, min(1.0, s * vol)) * 32767)
            w.writeframes(struct.pack('<h', val))


# Create only if missing
write_tone(os.path.join(SOUNDS_DIR, 'step.wav'), 0.08, 650, vol=0.7)
write_tone(os.path.join(SOUNDS_DIR, 'hit.wav'), 0.18, 180, vol=0.8)

# Simple short theme (concatenate three notes)
theme_path = os.path.join(MUSIC_DIR, 'theme.wav')
if not os.path.exists(theme_path):
    notes = [262, 330, 392, 330]
    sr = 22050
    with wave.open(theme_path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        for f in notes:
            dur = 0.35
            n = int(dur * sr)
            for i in range(n):
                t = i / sr
                s = math.sin(2 * math.pi * f * t)
                val = int(max(-1.0, min(1.0, s * 0.35)) * 32767)
                w.writeframes(struct.pack('<h', val))

print('Assets ensured (only missing files were created).')

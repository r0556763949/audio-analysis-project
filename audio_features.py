import librosa
import numpy as np

def extract_features(file_path):
    y, sr = librosa.load(file_path)

    # Energy
    rms = librosa.feature.rms(y=y)
    energy = float(np.mean(rms))

    # Speech rate
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    speech_rate = float(tempo[0])

    # Pitch variance (YIN)
    f0 = librosa.yin(y, fmin=50, fmax=300)
    f0 = f0[~np.isnan(f0)]
    pitch_variance = float(np.std(f0))

    # Pauses
    intervals = librosa.effects.split(y, top_db=20)
    total_sound = sum(end - start for start, end in intervals)
    total_length = len(y)
    pauses = 1 - (total_sound / total_length)

    # Fluency
    fluency = speech_rate * (1 - pauses) * (1 + pitch_variance / 200)

    return {
        "energy": energy,
        "speech_rate": speech_rate,
        "pitch_variance": pitch_variance,
        "pauses": pauses,
        "fluency": fluency
    }
import numpy as np
import librosa
import os

sr = 44100
duration = 5
samples = sr * duration

def read_audio(path):
    y, _ = librosa.core.load(path, sr=44100)
    
    # trim silence
    if 0 < len(y): # workaround: 0 length causes error
        y, _ = librosa.effects.trim(y)
    if len(y) > samples: # long enough
        y = y[0:0+samples]
    else: # pad blank
        padding = samples - len(y)
        offset = padding // 2
        y = np.pad(y, (offset, samples - len(y) - offset), 'constant')
    return y

def audio_to_melspectrogram(audio):
    
    spectrogram = librosa.feature.melspectrogram(audio, 
                                                 sr=sr)
    
    return librosa.power_to_db(spectrogram).astype(np.float32)

def read_as_melspectrogram(path):
    
    mels = audio_to_melspectrogram(read_audio(path))
    return mels

def convert_wav_to_image(df, path):
    X = []
    for _, row in df.iterrows():
        x = read_as_melspectrogram(os.path.join(path + row['audio']))
        X.append(x.transpose())
    
    return X

def normalize(img):
    eps = 0.001
    if np.std(img) != 0:
        img = (img - np.mean(img)) / np.std(img)
    else:
        img = (img - np.mean(img)) / eps
    return img

def normalize_dataset(X):
    normalized_dataset = []
    for img in X:
        normalized = normalize(img)
        normalized_dataset.append(normalized)
    return normalized_dataset
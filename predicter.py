# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from tensorflow import keras
import math
import librosa.display
from sklearn.preprocessing import StandardScaler
from collections import Counter

parts = 0


def load_song(path):
    y, sr = librosa.load(path, mono=True)
    duration = librosa.get_duration(y)

    global parts
    parts = math.floor(duration / 30.0)

    song_data = []
    for part in range(parts):
        y, sr = librosa.load(path, mono=True, offset=part * 30, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)

        features = [np.mean(chroma_stft), np.var(chroma_stft), np.mean(rmse), np.var(rmse), np.mean(spec_cent),
                    np.var(spec_cent), np.mean(spec_bw), np.var(spec_bw), np.mean(rolloff), np.var(rolloff),
                    np.mean(zcr), np.var(zcr)]

        for e in mfcc:
            features.append(np.mean(e))
            features.append(np.var(e))

        song_data.append(features)

    columns = ['chroma_stft', 'chroma_stft_var', 'rmse', 'rmse_var', 'spectral_centroid', 'spectral_centroid_var',
               'spectral_bandwidth', 'spectral_bandwith_var', 'rolloff', 'rolloff_var', 'zero_crossing_rate',
               'zero_crossing_rate_var']
    for i in range(1, 21):
        columns.append(f'mfcc{i}')
        columns.append(f'mfcc{i}_var')

    return pd.DataFrame(song_data, columns=columns)


def genre_mapping(index):
    switcher = {
        0: 'International',
        1: 'Pop',
        2: 'Rock',
        3: 'Electronic',
        4: 'Folk',
        5: 'Hip-Hop',
        6: 'Experimental',
        7: 'Instrumental'
    }

    return switcher.get(index, "no match")


def normalize_data(song):
    # Normalize
    # we need to load training_data to normalize new data accordingly
    data = pd.read_csv('./data/features_with_var_parentlabels.csv')
    data = data.drop(['filename', 'label'], axis=1)
    data = data.append(song)

    scaler = StandardScaler()
    return scaler.fit_transform(np.array(data, dtype=float))


def predict(X):
    # Load Model
    model = keras.models.load_model('music_genre_detector_model')

    predictions = model.predict(X)

    part_predictions = []
    for prt in range(parts):
        part_predictions.append(np.argmax(predictions[len(predictions) - (prt + 1)]))

    counted = Counter(part_predictions)
    for key in counted:
        print(str(genre_mapping(key)) + ': ' + str(counted[key] / len(part_predictions) * 100) + '%')

    return genre_mapping(max(part_predictions, key=part_predictions.count))

def eval(path):
    song = load_song(r"{}".format(path))
    X = normalize_data(song)
    print('Most parts of the song were categorized as ' + predict(X))



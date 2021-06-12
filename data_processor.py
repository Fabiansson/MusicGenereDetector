# -*- coding: utf-8 -*-
import librosa
import librosa.display
import numpy as np
import os
import csv
import xlrd
import multiprocessing as mp
import sys
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

# Path to training mp3 dataset. Note that all files must be in same directory without sub-directories
directory = r'E:\ML\fma_small\fma_small'


def setLabels():
    print("Creating labels...")
    d = {}
    wb = xlrd.open_workbook('./data/trackgenremapping.xlsx')
    sh = wb.sheet_by_index(0)
    for i in range(1, sh.nrows):
        val = int(sh.cell(i, 0).value)
        cell_value_class = f'{val:06}'
        cell_value_id = sh.cell(i, 1).value
        d[cell_value_class] = cell_value_id
    print("Labels created!")
    return d


labels = setLabels()


def featurize(filename):
    try:
        songname = os.path.join(directory, filename)

        sys.stdout.write("Generating representation of {} in folder {}".format(filename, directory))
        audioname = filename.split(".")[0]
        y, sr = librosa.load(songname, mono=True, duration=30)

        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)

        to_append = f'{filename} {np.mean(chroma_stft)} {np.var(chroma_stft)} {np.mean(rmse)} {np.var(rmse)} {np.mean(spec_cent)} {np.var(spec_cent)} {np.mean(spec_bw)} {np.var(spec_bw)} {np.mean(rolloff)} {np.var(rolloff)} {np.mean(zcr)} {np.var(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
            to_append += f' {np.var(e)}'
        to_append += f' {labels[audioname]}'

        return to_append
    except Exception as e:
        print("ERROR")
        print(e)
        return ''


if __name__ == "__main__":
    print("Creating csv..")

    output = 'features.csv'
    header = 'filename chroma_stft chroma_stft_var rmse rmse_var spectral_centroid spectral_centroid_var ' \
             'spectral_bandwidth spectral_bandwith_var rolloff rolloff_var zero_crossing_rate zero_crossing_rate_var '
    for i in range(1, 21):
        header += f' mfcc{i}'
        header += f' mfcc{i}_var'
    header += ' label'
    header = header.split()

    file = open(output, 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    print("CSV created!")

    N = 4  # number of cores to use
    print(N)
    files = os.listdir(directory)
    files_split = np.array_split(files, 6)

    for i in range(len(files_split)):
        with mp.Pool(processes=N) as p:
            results = list(tqdm(p.imap(featurize, files_split[0])))

        file = open(output, 'a', newline='')
        with file:
            for el in results:
                writer = csv.writer(file)
                writer.writerow(el.split())
        file.close()

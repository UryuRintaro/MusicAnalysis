import numpy as np
import madmom
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

data_dir = "data"
idx = 0
file_list = list(Path(data_dir).glob('*.wav'))

name = file_list[idx].stem
print(f"Processing: {name} ...")

print("     RNN Beat Processing ...")
activations = madmom.features.RNNBeatProcessor()(file_list[idx])

activations = zoom(activations,  2, order=1)
epsilon = 1e-8
activations = np.clip(activations, epsilon, 1.0 - epsilon)
# print(repr(activations))

print("     Tempo Estimation Processing ...")
tempo_estimation_processor = madmom.features.tempo.DBNTempoHistogramProcessor(min_bpm=60, max_bpm=250, fps=200)
bins, delays = tempo_estimation_processor(activations)

peak_idx = np.argmax(bins)
beat_lag = delays[peak_idx]

fps = 200
beat_bpm =  60.0 *  fps / beat_lag
print(f"max_peak: {bins[peak_idx]}, beat_lag: {beat_lag}, estimated tempo: {beat_bpm} BPM")

bpms = 60  *fps / delays
plt.plot(bpms, bins)
plt.savefig('tempo_histogram.png')



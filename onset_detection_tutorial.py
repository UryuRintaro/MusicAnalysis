import madmom
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import maximum_filter

path = 'ハッピー至上主義!.wav'
spec = madmom.audio.spectrogram.Spectrogram(path, num_channels=1)

print(spec.shape)
diff = np.diff(spec, axis=0)
pos_diff = np.maximum(0,diff)
sf = np.sum(pos_diff, axis=1)

sf = madmom.features.onsets.spectral_flux(spec)
fill_spec = madmom.audio.spectrogram.FilteredSpectrogram(spec, filter_bank=madmom.audio.filters.LogFilterbank, num_bands=24)
freqs = fill_spec.filterbank.center_frequencies
band_num = len(fill_spec.filterbank.center_frequencies)

cmap = plt.get_cmap('jet')
steps = 10

PEAK_THRESHOLD = 250.0
y_limit = np.max(fill_spec)
for i in range(band_num):
    color = cmap(i / band_num)
    data = fill_spec[:, i]
    current_freq = freqs[i]
    if i%steps == 0:
        label = f'{int(freqs[i])} Hz'
    else:
        label = '__nolegend__'
    plt.plot(fill_spec[:, i], color=color, linewidth=1, label=label, alpha=0.8)
    peaks, _ =  find_peaks(data, height=PEAK_THRESHOLD)
    for peak_idx in peaks:
        peak_val = data[peak_idx]
        plt.axvline(peak_idx, color='red', linestyle='-', linewidth=1.0, alpha=1)

plt.legend(
    loc='upper right',
    fontsize='small',
)
start = 500
step = 500
plt.xlim(start, start+step)
plt.savefig('spectral_flux_500_1000.png')
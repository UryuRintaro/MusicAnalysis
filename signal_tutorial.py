import madmom
from madmom import audio
from madmom.io.audio import load_wave_file
import matplotlib.pyplot as plt
import numpy as np

path = 'ハッピー至上主義!.wav'

fs = audio.signal.FramedSignal(path, frame_size=2048, hop_size=441, num_channels=1)
# print(f'frame  signal : {fs.shape}')
# print(f'sample  rate: {fs.signal.sample_rate}, signal : {fs.signal.shape}')

stft = 20 * np.log10(np.abs(audio.stft.STFT(fs)).T  + 1e-6)

# print(f'stft member:{vars(stft)}, stft shape: {stft.shape}')

spec = 20 * np.log10(audio.spectrogram.Spectrogram(path, frame=2048, hop_size=441, num_channels=1).T)
print(vars(spec.stft.frames.signal))

max_time = (len(fs.signal) / fs.signal.sample_rate) / 60
max_freq = fs.signal.sample_rate  / 2
extent = [0, max_time, 0, max_freq]

plt.imshow(spec, aspect='auto',  origin='lower', cmap='viridis', extent=extent)
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (sec)')
plt.colorbar(label='Magnitude (dB)')
plt.savefig('stft.png')

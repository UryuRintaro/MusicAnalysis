import madmom
import numpy as np
from pathlib import Path

data_dir = "data"
file_list = list(Path(data_dir).glob('*.wav'))
idx = 0
path = file_list[idx]
WINDOW_SIZE = 10.
STEP_SIZE = 5.

signal = madmom.audio.signal.Signal(path, num_channels=1)
sr = signal.sample_rate

key_processor =  madmom.features.key.CNNKeyRecognitionProcessor()

result = []
duration = len(signal) / sr

for start_time in np.arange(0, duration - WINDOW_SIZE, STEP_SIZE):
    end_time = start_time + WINDOW_SIZE
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)

    segment =signal[start_sample:end_sample]
    seg_signal = madmom.audio.signal.Signal(segment, sample_rate=sr)

    key_prob = key_processor(seg_signal)
    key_label = madmom.features.key.key_prediction_to_label(key_prob)
    result.append({
        "start": start_time,
        "end": end_time,
        "key": key_label
    })

print(f"{'Time':<15} | {'Estimated Key'}")
print("-" * 30)

prev_key = None
for item in result:
    time_str = f"{item['start']:.1f}s - {item['end']:.1f}s"
    current_key = item['key']
    
    marker = " <--- CHANGE" if (prev_key is not None and prev_key != current_key) else ""
    
    print(f"{time_str:<15} | {current_key}{marker}")
    prev_key = current_key


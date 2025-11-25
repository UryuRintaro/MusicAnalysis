import pandas as pd
from rich import print
from rich.table import Table
from rich.console import Console
import numpy as np
from pathlib import Path
import pandas as pd

data_prof = pd.read_json('data.json', orient='index')
data_dir = "data"
file_list = list(Path(data_dir).glob('*.wav'))
print("key list: ", list(data_prof.keys()))

# sort by any key values
# data_prof = data_prof.sort_values(by='bpm', ascending=False)

# Filtering by any key values
# data_prof = data_prof[data_prof['artist'].str.contains('Liella!')]

# condition search
# data_prof = data_prof[data_prof['duration']>4]

console = Console()
table = Table(title='music list')
table.add_column('ID', justify='center')
table.add_column('Song Name', justify='center')
for key in data_prof.keys():
    if key != 'id':
        table.add_column(key, justify='center')

for song_name, row in data_prof.iterrows():
    row_data = []
    row_data.append(str(int(row['id'])).zfill(2))
    row_data.append(song_name)
    for key in data_prof.keys():
        if key == 'id':
            continue
        val = row[key]
        if pd.isna(val):
            row_data.append("No data")
        elif isinstance(val, float) and key != 'duration':
            row_data.append(str(int(val)))
        elif key == 'duration':
            row_data.append(f"{val:.2f}")
        else:
            row_data.append(str(val))
    table.add_row(*row_data)

console.print(table)

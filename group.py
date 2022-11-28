import os
import pandas as pd 
import shutil
from tqdm import tqdm

path = 'ECGDataDenoised'
df = pd.read_excel('Diagnostics.xlsx', index_col='FileName')

if not os.path.exists(path):
    raise FileNotFoundError("Extract ECGDataDenoised.zip")

if os.path.exists("Data"):
    shutil.rmtree("Data")
os.mkdir("Data")
os.mkdir("Data/AF")
os.mkdir("Data/NORMAL")

files = []
count = 0
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in tqdm(f):
        if '.csv' in file:
            name = file[:-4]
            # print(name)
            rhy = df.loc[name, 'Rhythm']
            if rhy in ['AF', 'AFIB']:
                shutil.move(os.path.join(r, file), f'Data/AF/{file}')
            else:
                shutil.move(os.path.join(r, file), f'Data/NORMAL/{file}')
            files.append(os.path.join(r, file))
            count+= 1
            # print(count)
        
shutil.rmtree(path)
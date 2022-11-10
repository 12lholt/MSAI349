import os
import pandas as pd 
import shutil

path = '/Users/xyan/Desktop/code/ML PROJ/ECGDataDenoised'
df = pd.read_excel('Diagnostics.xlsx', index_col='FileName')

files = []
count = 0
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            name = file[:-4]
            print(name)
            rhy = df.loc[name, 'Rhythm']
            if rhy in ['AF', 'AFIB']:
                shutil.copy(os.path.join(r, file), '/Users/xyan/Desktop/code/ML PROJ/AF')
            else:
                shutil.copy(os.path.join(r, file), '/Users/xyan/Desktop/code/ML PROJ/NORMAL')
            files.append(os.path.join(r, file))
            count+= 1
            print(count)


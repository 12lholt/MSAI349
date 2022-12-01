from glob import glob
import pandas as pd
import numpy as np
import torch
from tqdm import tqdm
import math
import matplotlib.pyplot as plt
import plotly.express as px
import sys
import random

class CreateDataset():
    def __init__(self, data_path:str="Data", roll_size:int=1500, stride:int=750, size_limit:float=3.204,
        normal_file_factor:int=1, device:torch.device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):

        self.roll_size = roll_size
        self.stride = stride
        self.af_files = glob(data_path+"/AF/*.csv")
        self.normal_files = glob(data_path+"/NORMAL/*.csv")
        self.n_files = int(size_limit/(math.ceil((5000-roll_size)/stride)*roll_size*12*8*1e-9))
        self.n_files = min(self.n_files, len(self.af_files)*(1+normal_file_factor))
        self.af_files = random.sample(self.af_files, int(self.n_files/(1+normal_file_factor)))
        self.normal_files = random.sample(self.normal_files, int(normal_file_factor*self.n_files/(1+normal_file_factor)))
        self.device = device
    
    def roll(self, df:pd.DataFrame):
        return torch.from_numpy(df.to_numpy()).unfold(0, self.roll_size, self.stride).to(self.device)

    def log_transform(self, df:pd.DataFrame):
        return np.abs(df)/df*np.log10(np.abs(df)+1)
    
    def min_max(self, df:pd.DataFrame):
        return df/abs(df).max(axis="rows")
    
    def files_process(self):
        x = list()
        y = list()
        nc=0
        for af in tqdm(self.af_files):
            df = pd.read_csv(af, header=None)
            df = self.log_transform(df)
            df = self.min_max(df)
            df = self.roll(df)
            if torch.isnan(df).any():
                nc+=1
                continue
            x.append(df)
            y+=[1]*x[-1].shape[0]
        for normal in tqdm(self.normal_files):
            df = pd.read_csv(normal, header=None)
            df = self.log_transform(df)
            df = self.min_max(df)
            df = self.roll(df)
            if torch.isnan(df).any():
                nc+=1
                continue
            x.append(df)
            y+=[0]*x[-1].shape[0]
        x = torch.concat(x)
        y = torch.Tensor(y)
        print(nc)
        return torch.utils.data.TensorDataset(x.unsqueeze(1), y.unsqueeze(1))

if __name__=="__main__":
    torch.save(CreateDataset(device=torch.device("cpu")).files_process(), "vars/dataset3.pt")
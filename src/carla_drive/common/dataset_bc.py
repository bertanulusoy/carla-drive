import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os

from PIL import Image 

class BCDataset(Dataset):
    def __init__(self, data_path):
        """
        data_path: Kaydedilen verilerin (resimler ve aksiyonlar) olduğu klasör.
        """
        self.data_path = data_pathself.filenames = [f for f in os.listdir(data_path) if f.endswith('.png')]

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        # Resmi yükle
        img_path = os.path.join(self.data_path, self.filenames[idx])
        image = Image.open(img_path).convert('RGB')
        image = np.array(image).transpose((2, 0, 1)) / 255.0  # Normalize ve CHW formatına çevir

        # Aksiyon dosyasını yükle
        action_path = img_path.replace('.png', '.npy')
        action = np.load(action_path)

        return torch.tensor(image, dtype=torch.float32), torch.tensor(action, dtype=torch.float32)

    def __getitem__(self, idx):
        # Resmi yükle
        img_path = os.path.join(self.data_path, self.filenames[idx])
        image = Image.open(img_path).convert('RGB')
        image = np.array(image).transpose((2, 0, 1)) / 255.0  # Normalize ve CHW formatına çevir

        # Aksiyon dosyasını yükle
        action_path = img_path.replace('.png', '.npy')
        action = np.load(action_path)

        return torch.tensor(image, dtype=torch.float32), torch.tensor(action, dtype=torch.float32)

        return image, action

if __name__ == "__main__":

    pass
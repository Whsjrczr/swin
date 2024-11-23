import os
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets

class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        self._load_data()

    def _load_data(self):
        index = 0
        for label_dir in os.listdir(self.root_dir):
            label_dir_path = os.path.join(self.root_dir, label_dir)
            if os.path.isdir(label_dir_path):
                for image_name in os.listdir(label_dir_path):
                    image_path = os.path.join(label_dir_path, image_name)
                    self.image_paths.append(image_path)
                    self.labels.append(index)  # 假设文件夹名即为标签
            index += 1

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = datasets.folder.default_loader(image_path)
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

def make_dataset(root_dir, train_transform, test_transform, splite_rate):
    full_dataset = CustomDataset(root_dir=root_dir, transform=train_transform)
    train_size = int((1 - splite_rate) * len(full_dataset))
    test_size = int(splite_rate * len(full_dataset))
    train_dataset, _ = torch.utils.data.random_split(full_dataset, [train_size, test_size])
    full_dataset = CustomDataset(root_dir=root_dir, transform=test_transform)
    _, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])
    return train_dataset, test_dataset
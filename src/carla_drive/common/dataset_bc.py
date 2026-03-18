import argparse
import os

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from PIL import Image


class BCDataset(Dataset):
    """Behavior cloning dataset.

    Expects data_path to contain pairs of files:
      - image files ending with `.png`
      - corresponding action files with the same stem and `.npy` extension

    Example:
      000001.png
      000001.npy
    """

    def __init__(self, data_path: str, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.filenames = sorted([f for f in os.listdir(data_path) if f.lower().endswith('.png')])

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_path = os.path.join(self.data_path, self.filenames[idx])
        image = Image.open(img_path).convert('RGB')

        if self.transform is not None:
            image = self.transform(image)
        else:
            # Default: normalize to [0, 1] and return CHW float tensor
            image = np.array(image).astype(np.float32) / 255.0
            image = image.transpose((2, 0, 1))
            image = torch.from_numpy(image)

        action_path = img_path.replace('.png', '.npy')
        action = np.load(action_path).astype(np.float32)
        action = torch.from_numpy(action)

        return image, action


class BCModel(nn.Module):
    """Simple CNN to map camera images to actions."""

    def __init__(self, num_outputs: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, num_outputs),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def train_bc(
    data_path: str,
    epochs: int = 10,
    batch_size: int = 32,
    lr: float = 1e-3,
    device: str = "cpu",
    save_path: str | None = None,
):
    dataset = BCDataset(data_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

    sample_action = dataset[0][1]
    model = BCModel(num_outputs=sample_action.shape[0]).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0

        for images, actions in dataloader:
            images = images.to(device)
            actions = actions.to(device)

            preds = model(images)
            loss = criterion(preds, actions)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch}/{epochs} - loss: {epoch_loss:.6f}")

    if save_path:
        torch.save(model.state_dict(), save_path)
        print(f"Saved model to {save_path}")

    return model


def _parse_args():
    parser = argparse.ArgumentParser(description="Train a behavior cloning model from image+action pairs.")
    parser.add_argument("data_path", help="Folder containing .png images and .npy actions")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--save", default=None, help="Path to save trained model weights")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    train_bc(
        data_path=args.data_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        save_path=args.save,
    )


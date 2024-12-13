import torch
from torch.utils.data import Dataset, DataLoader


class ImitationDataset(Dataset):
    def __init__(self, demonstrations):
        self.states = []
        self.actions = []

        for demo in demonstrations:
            self.states.extend(demo["states"])
            self.actions.extend(demo["actions"])

        self.states = torch.tensor(self.states, dtype=torch.float32)
        self.actions = torch.tensor(self.actions, dtype=torch.long)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return self.states[idx], self.actions[idx]

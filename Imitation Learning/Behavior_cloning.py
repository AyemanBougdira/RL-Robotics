import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


class BCModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(BCModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )

    def forward(self, x):
        return self.net(x)


def train_bc_model(dataset, input_dim, output_dim, epochs=50, batch_size=32):
    """
    Entraîne un modèle Behavior Cloning.
    
    Args:
        dataset: Dataset d'imitation.
        input_dim: Dimension des états.
        output_dim: Dimension des actions.
        epochs: Nombre d'époques d'entraînement.
        batch_size: Taille du batch.
    """
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    model = BCModel(input_dim, output_dim)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for states, actions in dataloader:
            optimizer.zero_grad()
            outputs = model(states)
            loss = loss_fn(outputs, actions)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs} - Loss: {total_loss:.4f}")

    return model

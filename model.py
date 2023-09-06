import torch

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.input = torch.nn.Linear(5, 15)
        self.relu = torch.nn.ReLU()
        self.output = torch.nn.Linear(15, 1)
        self.af = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.input(x)
        x = self.relu(x)
        x = self.output(x)
        return self.af(x)
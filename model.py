import torch

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.input = torch.nn.Linear(5, 10)
        self.relu = torch.nn.ReLU()
        self.hidden = torch.nn.Linear(10, 5)
        self.output = torch.nn.Linear(5, 1)
        self.af = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.input(x)
        x = self.relu(x)
        x = self.hidden(x)
        x = self.relu(x)
        x = self.output(x)
        return self.af(x)
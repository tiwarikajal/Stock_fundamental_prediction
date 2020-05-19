
##Import Required packages
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torch.utils.data as Data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import imageio
import os, sys
import pandas as pd
import re
import seaborn as sns
from tqdm.notebook import tqdm
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

filepath=r'/mnt/nfs/scratch1/kajaltiwari/data/'
# Read and create dataframe
final_df = pd.read_pickle('Final_Dataset_max.pkl')

# Test Train Split
x = final_df['x']
y = final_df['y']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=False)
y_train, y_test = y_train.astype(float), y_test.astype(float)

# DataLoader
n_train = X_train.shape[0]
n_test = X_test.shape[0]
X_train = torch.tensor(X_train, dtype=torch.float)
Y_train = torch.tensor(y_train, dtype=torch.float).view(-1, 1)
datasets = torch.utils.data.TensorDataset(X_train, Y_train)
train_iter = torch.utils.data.DataLoader(datasets, batch_size=10, shuffle=True)

# Parameters
EPOCHS = 10000
BATCH_SIZE = 1
LEARNING_RATE = 0.00005
NUM_FEATURES = 3074


# Model
class Regression(nn.Module):
    def __init__(self, num_features):
        super(Regression, self).__init__()

        self.layer_1 = nn.Linear(num_features, 768)
        self.layer_2 = nn.Linear(768, 768)
        self.layer_out = nn.Linear(768, 1)
        self.relu = nn.ELU()
        # self.relu = nn.Tanh()
        # self.relu=nn.Sigmoid()

    def forward(self, inputs):
        x = self.relu(self.layer_1(inputs))
        # x=self.layer_1(inputs)
        y = self.relu(self.layer_2(x))
        z = self.layer_out(y)
        return (z)


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = Regression(NUM_FEATURES)
model.to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
loss = []

# Training

for e in range(1, EPOCHS + 1):

    # TRAINING
    train_epoch_loss = 0
    model.train()

    for x, y in train_iter:
        output = model(x.cuda())
        train_loss = criterion(output, y.cuda())
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        train_epoch_loss += train_loss.item()

    loss.append(train_epoch_loss)

y_pred_list = []
f = open(filepath + "Results.txt", 'w')
with torch.no_grad():
    model.eval()
    for x in X_test.to_numpy():
        y_test_pred = model(torch.tensor(x).float().cuda())
        y_pred_list.append(y_test_pred.cpu())
y_pred_list = [n.squeeze().tolist() for n in y_pred_list]
mse = mean_squared_error(y_test.to_numpy(), y_pred_list)
y_test = y_test.to_numpy()
r_square = r2_score(y_test, y_pred_list)
f.write("\n Y_pred is \n" + y_pred_list)
f.write("\n Y_target is \n" + y_test)
f.write("\nMean Squared Error\n :", mse)
f.write("\nR^2Error\n :", r_square)
f.write("\n")
f.close()

import argparse
import random

import torch
import torch.nn as nn
import torch.optim as optim

from model import GGNN
from model import CNN
from model import GatedCNN
from model import STGCBlock
from utils.train import train
from utils.test import test
from utils.data.dataset import NBADataset
from utils.data.dataloader import NBADataloader

parser = argparse.ArgumentParser()
parser.add_argument('--L', type=int, help='number of past timesteps', default=2)
parser.add_argument('--model', type=int, help='0:ggnn, 1:cnn, 2:gatedcnn, 3:stgcblock', default=0)
parser.add_argument('--classes', type=int, help='number of output_dim', default=0)
parser.add_argument('--task', type=int, help='0:att0, 1:att1, 2:att2, 3:att3, 4:lost, 5:return, 6:multi', default=0)
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=1, help='input batch size')
parser.add_argument('--state_dim', type=int, default=45, help='GGNN hidden state size')
parser.add_argument('--n_steps', type=int, default=5, help='propogation steps number of GGNN')
parser.add_argument('--niter', type=int, default=20, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--cuda', action='store_true', help='enables cuda')
parser.add_argument('--verbal', action='store_true', help='print training info or not')
parser.add_argument('--manualSeed', type=int, help='manual seed')


opt = parser.parse_args()
print(opt)

if opt.manualSeed is None:
    opt.manualSeed = random.randint(1, 10000)
print("Random Seed: ", opt.manualSeed)
random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)

opt.dataroot = 'nba_data/L%d.npy' % opt.L

if opt.cuda:
    torch.cuda.manual_seed_all(opt.manualSeed)

def main(opt):
    train_dataset = NBADataset(opt.dataroot, True)
    train_dataloader = NBADataloader(train_dataset, batch_size=opt.batchSize, \
                                      shuffle=True, num_workers=opt.workers)

    test_dataset = NBADataset(opt.dataroot, False)
    test_dataloader = NBADataloader(test_dataset, batch_size=opt.batchSize, \
                                     shuffle=False, num_workers=opt.workers)

    opt.annotation_dim = 45  # for NBA
    opt.n_edge_types = train_dataset.n_edge_types
    opt.n_node = train_dataset.n_node
    opt.n_timesteps = opt.n_edge_types - 1

    model = STGCBlock(opt.state_dim, opt.annotation_dim, opt.n_edge_types, opt.n_timesteps, opt.n_node, opt.n_steps, opt.batchSize, opt.model)

    model.double()
    print(model)

    if opt.cuda:
        model.cuda()

    optimizer = optim.Adam(model.parameters(), lr=opt.lr)

    for epoch in range(0, opt.niter):
        train(epoch, train_dataloader, model, optimizer, opt)
        test(test_dataloader, model, optimizer, opt)

if __name__ == "__main__":
    main(opt)

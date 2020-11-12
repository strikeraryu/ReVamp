import os, sys

os.chdir(os.path.dirname(__file__))

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from PIL import Image
from skimage import io, transform
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from data_loader import RescaleT, ToTensorLab
from model import BASNet



model_dir = 'saved_model/basnet.pth'

net = None
BASNet_loaded = False

def load_BASNet():
    global net, BASNet_loaded
    
    if BASNet_loaded:
        print('BASNet is already loaded')
    else:
        print("Loading BASNet...")
        net = BASNet(3, 1)
        net.load_state_dict(torch.load(model_dir))
        if torch.cuda.is_available():
            net.cuda()
        net.eval()


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)
    return dn


def preprocess(image):
    label_3 = np.zeros(image.shape)
    label = np.zeros(label_3.shape[0:2])

    if (3 == len(label_3.shape)):
        label = label_3[:, :, 0]
    elif (2 == len(label_3.shape)):
        label = label_3

    if (3 == len(image.shape) and 2 == len(label.shape)):
        label = label[:, :, np.newaxis]
    elif (2 == len(image.shape) and 2 == len(label.shape)):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]

    transform = transforms.Compose([RescaleT(256), ToTensorLab(flag=0)])
    sample = transform({'image': image, 'label': label})

    return sample


def run(img):
    torch.cuda.empty_cache()

    sample = preprocess(img)
    inputs_test = sample['image'].unsqueeze(0)
    inputs_test = inputs_test.type(torch.FloatTensor)

    if torch.cuda.is_available():
        inputs_test = Variable(inputs_test.cuda())
    else:
        inputs_test = Variable(inputs_test)

    d1, d2, d3, d4, d5, d6, d7, d8 = net(inputs_test)

    # Normalization.
    pred = d1[:, 0, :, :]
    predict = normPRED(pred)

    # Convert to PIL Image
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()
    im = Image.fromarray(predict_np * 255).convert('RGB')

    # Cleanup.
    del d1, d2, d3, d4, d5, d6, d7, d8

    return im



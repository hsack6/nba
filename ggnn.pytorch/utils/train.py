import torch
import torch.nn as nn
from torch.autograd import Variable

def train(epoch, dataloader, model, optimizer, opt):
    model.train()
    criterion = nn.CrossEntropyLoss()
    if opt.cuda:
        criterion.cuda()

    for i, (annotation, am, label_attribute, label_lost, label_return) in enumerate(dataloader, 0):
        model.zero_grad()

        init_input = annotation
        batch_size = init_input.shape[0]
        n_node = init_input.shape[1]

        if opt.cuda:
            init_input = init_input.cuda()
            annotaion = annotation.cuda()
            am = am.cuda()
            label_attribute = label_attribute.cuda()
            label_lost = label_lost.cuda()
            label_return = label_return.cuda()

        init_input = Variable(init_input)
        annotation = Variable(annotation)
        am = Variable(am)
        label_attribute = Variable(label_attribute)
        label_lost = Variable(label_lost)
        label_return = Variable(label_return)

        output = model(init_input, annotation, am)
        target = label_attribute.transpose(0,2).transpose(1,2)[0].contiguous()

        output = output.view(batch_size*n_node, 31)
        target = target.view(batch_size*n_node,   ).long()

        loss = criterion(output, target)

        loss.backward()
        optimizer.step()

        if i % int(len(dataloader) / 10 + 1) == 0 and opt.verbal:
            print('[%d/%d][%d/%d] Loss: %.4f' % (epoch, opt.niter, i, len(dataloader), loss.data[0]))

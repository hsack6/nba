import torch
import torch.nn as nn
from torch.autograd import Variable

def test(dataloader, model, optimizer, opt):
    test_loss = 0
    correct = 0
    criterion = nn.CrossEntropyLoss()
    model.eval()
    if opt.cuda:
        criterion.cuda()
    for i, (annotation, am, label_attribute, label_lost, label_return) in enumerate(dataloader, 0):
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

        test_loss += criterion(output, target).data[0]
        #print(output.data.max(1, keepdim=True)[1].size()) (860, 1)
        pred = output.data.max(1, keepdim=True)[1]
        #print(pred)
        #print(target.data.view_as(pred).size()) (860, 1)
        #print(pred.eq(target.data.view_as(pred)).size()) (860, 1)
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(dataloader.dataset)
    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)'.format(
        test_loss, correct, n_node * len(dataloader.dataset),
        100. * correct / (n_node * len(dataloader.dataset))))

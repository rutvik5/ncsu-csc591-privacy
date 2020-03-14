import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import syft as sy 
import random 

# class Arguments():
#     def __init__(self):
#         self.batch_size = 128
#         self.test_batch_size = 1000
#         self.epochs = 1
#         self.lr = 0.01
#         self.momentum = 0.5
#         self.no_cuda = True
#         self.seed =  ## TODO change seed to your studentID inside the class Arguments (line 17)
#         self.log_interval = 30
#         self.save_model = False

# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(1, 20, 5, 1)
#         self.conv2 = nn.Conv2d(20, 50, 5, 1)
#         self.fc1 = nn.Linear(4*4*50, 500)
#         self.fc2 = nn.Linear(500, 10)

#     def forward(self, x):
#         x = F.relu(self.conv1(x))
#         x = F.max_pool2d(x, 2, 2)
#         x = F.relu(self.conv2(x))
#         x = F.max_pool2d(x, 2, 2)
#         x = x.view(-1, 4*4*50)
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return F.log_softmax(x, dim=1)


# def train(args, model, device, federated_train_loader, optimizer, epoch, participates):
#     model.train()  # <-- initial training
#     for batch_idx, (data, target) in enumerate(federated_train_loader): # <-- now it is a distributed dataset
#         if target.location.id in participates:
#             model.send(data.location) # <-- NEW: send the model to the right location
#             data, target = data.to(device), target.to(device)
#             optimizer.zero_grad()
#             output = model(data)
#             loss = F.nll_loss(output, target)
#             loss.backward()
#             optimizer.step()
#             model.get() # <-- NEW: get the model back
#             if batch_idx % args.log_interval == 0:
#                 loss = loss.get() # <-- NEW: get the loss back
#                 print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
#                     epoch, batch_idx * args.batch_size, len(federated_train_loader) * args.batch_size,
#                     100. * batch_idx / len(federated_train_loader), loss.item()))


            
# def test(args, model, device, test_loader):
#     model.eval()
#     test_loss = 0
#     correct = 0
#     with torch.no_grad():
#         for data, target in test_loader:
#             data, target = data.to(device), target.to(device)
#             output = model(data)
#             test_loss += F.nll_loss(output, target, reduction='sum').item() # sum up batch loss
#             pred = output.argmax(1, keepdim=True) # get the index of the max log-probability 
#             correct += pred.eq(target.view_as(pred)).sum().item()

#     test_loss /= len(test_loader.dataset)

#     print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
#         test_loss, correct, len(test_loader.dataset),
#         100. * correct / len(test_loader.dataset)))


# ### main function

# args = Arguments()
# use_cuda = not args.no_cuda and torch.cuda.is_available()
# torch.manual_seed(args.seed) 
# device = torch.device("cuda" if use_cuda else "cpu")
# kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

# hook = sy.TorchHook(torch)  # <-- NEW: hook PyTorch ie add extra functionalities to support Federated Learning

# ## TODO: ----  create 10 node workers  ---- ##


# ##-------------------------------------------

# ## distribute data across nodes
# federated_train_loader = sy.FederatedDataLoader( # <-- this is now a FederatedDataLoader 
#     datasets.MNIST('./data', train=True, download=True,
#                    transform=transforms.Compose([
#                        transforms.ToTensor(),
#                        transforms.Normalize((0.1307,), (0.3081,))
#                    ]))
#     .federate((  )), ##TODO: pass the worker nodes you created here to distribute the data
#     batch_size=args.batch_size, shuffle=True, **kwargs)

# ## test dataset is always same at the central server
# test_loader = torch.utils.data.DataLoader(
#     datasets.MNIST('./data', train=False, transform=transforms.Compose([
#                        transforms.ToTensor(),
#                        transforms.Normalize((0.1307,), (0.3081,))
#                    ])),
#     batch_size=args.test_batch_size, shuffle=True, **kwargs)

# ## training models in a federated appraoch
# model = Net().to(device)
# optimizer = optim.SGD(model.parameters(), lr=args.lr) 

# ## TODO: select a random set of node ids that will be passed to the training function; these nodes will particiapte in the federated learning
# #create node_list 

# ##-------------------------------------------

# for epoch in range(1, args.epochs + 1):
#     train(args, model, device, federated_train_loader, optimizer, epoch, ) ## TODO: pass the node_id list like ['node1','node2' ...]
#     test(args, model, device, test_loader)

# if (args.save_model):
#     torch.save(model.state_dict(), "mnist_cnn.pt")







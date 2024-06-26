import numpy as np
import torch
import random
from collections import deque
import torch.optim as optim
import torch.nn.functional as F

class NeuralNetwork(torch.nn.Module):
    def __init__(self, input_layer, output_layer): #input layer 63? output layer 4 for now
        super(NeuralNetwork, self).__init__()
        self.fc1 = torch.nn.Linear(input_layer, 64)
        self.fc2 = torch.nn.Linear(64, output_layer)
        #self.fc3 = torch.nn.Linear(128, output_layer)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        #x = torch.relu(self.fc2(x))
        x = self.fc2(x)
        return x

BUFFER_SIZE = 50_000
BATCH_SIZE = 32


class Memory():
    def __init__(self, policy_model, target_model, gamma, learning_rate):
        self.memory = deque(maxlen=BUFFER_SIZE)
        self.batch_size = BATCH_SIZE
        self.policy_model = policy_model
        self.target_model = target_model
        self.gamma = gamma
        self.loss_function = torch.nn.MSELoss()
        self.learning_rate = learning_rate
        self.optimizer = optim.Adam(policy_model.parameters(), lr=self.learning_rate)
        self.loss = 0

    def update_memory(self,state,action,reward,new_state,done):
        self.memory.append((state,action,reward,new_state,done))

    def sample(self):
        return random.sample(self.memory, BATCH_SIZE)
    
    def train_from_memory(self, sample):
        states, actions, rewards, new_states, dones = zip(*sample)
        
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        new_states = torch.tensor(new_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        q_values_policy = self.policy_model(states)
        q_values_target = self.target_model(new_states)

        targets_values = q_values_policy.clone().detach()

        for i in range(len(sample)):
            next_q_value = torch.max(q_values_target[i]).item()
            targets_values[i, actions[i]] = rewards[i] + self.gamma * next_q_value * (~dones[i])
        
        loss = self.loss_function(q_values_policy, q_values_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
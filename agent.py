import numpy as np
import torch
import random
from collections import deque
from game import Game


class NeuralNetwork(torch.nn.Module):
    def __init__(self, input_layer, output_layer): #input layer 63? output layer 4 for now
        super(NeuralNetwork, self).__init__()
        self.fc1 = torch.nn.Linear(input_layer, 128)
        self.fc2 = torch.nn.Linear(128, 128)
        self.fc3 = torch.nn.Linear(128, output_layer)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

policy = NeuralNetwork(63,4)
target = NeuralNetwork(63,4)

inputs = torch.rand(1,63)

target.load_state_dict(policy.state_dict())


class Agent():

    def __init__(self, game):
        self.epsilon = 1.0
        self.DISCOUNT = 0.99
        self.EPISODES = 1000
        self.LEARNING_RATE = 0.01
        self.reward = 10
        self.penalty = -100
        self.game = game
        self.ACTIONS = {"rotate": 0,
                        "left": 1,
                        "right": 2,
                        "down": 3,
                        "hold": 4}
        
    

    def get_action(self,action_number):
        if action_number == 0:
            game.tetris.tetromino.rotate()
        elif action_number == 1:
            game.tetris.tetromino.move(direction="left")
        elif action_number == 2:
            game.tetris.tetromino.move(direction="right")
        elif action_number == 3:
            game.tetris.tetromino.move(direction="down")
        elif action_number == 4:
            pass
    
    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(4)  
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.policy_net(state)
        return torch.argmax(q_values).item()

    def train(self):
        for _ in range(self.EPISODES):
            pass
    
 


if __name__=="__main__":
    game = Game()
    agent = Agent(game)
    while True:
        game.run()
        
        
import numpy as np
import torch
import random
from game import Game
from network import NeuralNetwork, Memory
import itertools
import matplotlib.pyplot as plt

class Agent():

    def __init__(self, game):
        self.epsilon = 1.0
        self.gamma = 0.95
        self.learning_rate = 0.01
        self.EPISODES = 1000
        self.game = game
        self.ACTIONS = {"rotate": 0,
                        "left": 1,
                        "right": 2,
                        "down": 3,
                        "hold": 4}
        self.policy_net = NeuralNetwork(208,5)
        self.target_net = NeuralNetwork(208,5)
        self.memory = Memory(self.policy_net, self.target_net, self.gamma,self.learning_rate)

    

    def make_action(self,action_number):
        if action_number == 0:
            self.game.tetris.tetromino.rotate()
        elif action_number == 1:
            self.game.tetris.tetromino.move(direction="left")
        elif action_number == 2:
            self.game.tetris.tetromino.move(direction="right")
        elif action_number == 3:
            self.game.tetris.tetromino.move_down()
            
        elif action_number == 4:
            pass

    def get_state(self):
        #blocks_position = tf.keras.layers.Flatten(self.game.tetris.list_of_tetrominos)
        #block_position1d = [item for sublist in self.game.tetris.list_of_tetrominos for item in sublist]
        block_position1d = [1 if item != 0 else 0 for sublist in self.game.tetris.list_of_tetrominos for item in sublist]

        state = [
            # position of the tetromino blocks
            self.game.tetris.tetromino.blocks[0].position.x,
            self.game.tetris.tetromino.blocks[1].position.x,
            self.game.tetris.tetromino.blocks[2].position.x,
            self.game.tetris.tetromino.blocks[3].position.x,
            self.game.tetris.tetromino.blocks[0].position.y,
            self.game.tetris.tetromino.blocks[1].position.y,
            self.game.tetris.tetromino.blocks[2].position.y,
            self.game.tetris.tetromino.blocks[3].position.y,
            # game board
            #blocks_position
            # game speed
            #speed = 100



        ]
        state = state + block_position1d
        return np.array(state, dtype=np.float64)
    
    def act(self, state):
        if random.random() <= self.epsilon:
            print("random")
            return random.randint(0,4)  
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.policy_net(state)
            print("siec")
        return torch.argmax(q_values).item()

MIN_MEMORY_SIZE = 1_000
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 20_000

UPDATE_FREQ = 100
def train():
       
        
        game = Game()
        agent = Agent(game)
        
        for _ in range(5000):
            game.run()
            #print("Episode nr: ", _)
            state = agent.get_state()
            #print("JDJDJDJDJDJDJDJ",type(state))
            action = agent.act(state=state)
            agent.make_action(action)

            reward, done, score = game.tetris.check_for_reward()
            
            new_state = agent.get_state()
            
            agent.memory.update_memory(state,action,reward,new_state,done)
            # if _ == 1:
            #     print(agent.memory.memory)
            if done:
                game.restart()
                print("record: ",game.tetris.highscore)
        
        game.restart()
        
        for step in itertools.count():
            if len(agent.memory.memory) < MIN_MEMORY_SIZE:
                return
            game.run()
            epsilon = np.interp(step, [0, EPSILON_DECAY], [EPSILON_START, EPSILON_END])
            agent.epsilon = epsilon

            state = agent.get_state()
            
            action = agent.act(state)
            agent.make_action(action)

            reward, done, score = game.tetris.check_for_reward()

            if score > game.tetris.highscore:
                reward = 10
            
            new_state = agent.get_state()
            agent.memory.update_memory(state,action,reward,new_state,done)

            sample = agent.memory.sample()
            agent.memory.train_from_memory(sample)

            if step % UPDATE_FREQ == 0:
                agent.target_net.load_state_dict(agent.policy_net.state_dict())
            
            if done:
                game.restart()

                if score > game.tetris.highscore:
                    game.tetris.highscore = score

if __name__=="__main__":
    
    while True:
        train()
            
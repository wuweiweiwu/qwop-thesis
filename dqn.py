import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from qwop_env import QWOPEnv

EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        # input dim
        self.state_size = state_size
        # output dim
        self.action_size = action_size
        # queue for remembering past actions
        self.memory = deque(maxlen=2000)
        # decay to calculate future discounted reward
        self.gamma = 0.95    # discount rate
        # exploration rate, rate that the agent randomly decides rather than predict
        self.epsilon = 1.0  # exploration rate
        # exploe at least this amoutn
        self.epsilon_min = 0.01
        # decrease exploration as we get better and better
        self.epsilon_decay = 0.995
        # how much the neural net learns in each iteration
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # if random is less tahn exploration rate, we should guess
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # otherwise lets predict something
        act_values = self.model.predict(state)
        # returns the index with the highest value
        return np.argmax(act_values[0])  # returns action

    # play back previous batch_size actions and states
    def replay(self, batch_size):
        # randomly sample batch_size from self.memory
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                # predict the future discount reward
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))

            # map the current state to the future discounted reward
            target_f = self.model.predict(state)
            target_f[0][action] = target

            # train the neural net based on those values
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    # the gym environment
    # env = gym.make('CartPole-v1')
    env = QWOPEnv()
    # input dimensions
    # state_size = env.observation_space.shape[0]
    state_size = env.observation_space
    # output dimensions
    # action_size = env.action_space.n
    action_size = env.action_space
    # create dqn agent
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 32

    #file to write distance
    score_file = open('scores.txt', 'w+')
    moves_file = open('moves.txt', 'w+')
    distance_file = open('distances.txt', 'w+')

    # run 1000 episodes
    for e in range(EPISODES):
        # reset the environment
        state = env.reset()
        print "reset:", state
        # reshape so its the same dimension as the input to our agent
        state = np.reshape(state, [1, state_size])
        # play till score = 500
        # for qwoppy play 500 steps or until done
        for time in range(500):
            # show the environment
            # env.render()
            # ge the action that the agent predicts based on current state
            action = agent.act(state)
            # print action
            # apply the action and get the new state
            # next_state, reward, done, _ = env.step(action)
            next_state, reward, done, move = env.step(action)
            moves_file.write(move)
            # print next_state, reward, done
            distance = reward
            # if it is done then reward = -10 else its the reward
            reward = reward if not done else -10
            print "reward: ", reward
            # reshape the new stage
            next_state = np.reshape(next_state, [1, state_size])
            # print next_state

            # make the agent remember this action and state and new state
            agent.remember(state, action, reward, next_state, done)

            # current state = new state
            state = next_state
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}, distance: {}"
                      .format(e, EPISODES, time, agent.epsilon, distance))
                score_file.write('{}\n'.format(time))
                moves_file.write('\n')
                distance_file.write('{}\n'.format(distance))
                break
        # agent remember the past batch_size actions and states
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % 10 == 0:
            agent.save("./save/qwop-dqn.h5")
    score_file.close()
    moves_file.close()
    distance_file.close()

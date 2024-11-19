import numpy as np
from behaviour import *

class RLAgent:
    def __init__(self, player_id, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.player_id = player_id
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = np.zeros((14, 14))  # 13 cards + 1 for the tie state
        self.cards_left = [True] * 14

    def choose_action(self, treasure):
        if np.random.rand() < self.epsilon:
            action = np.random.choice(np.where(self.cards_left)[0])
        else:
            action = np.argmax(self.q_table[treasure])
        return action

    def update_q_table(self, treasure, action, reward, next_treasure):
        best_next_action = np.argmax(self.q_table[next_treasure])
        td_target = reward + self.gamma * self.q_table[next_treasure, best_next_action]
        td_error = td_target - self.q_table[treasure, action]
        self.q_table[treasure, action] += self.alpha * td_error

    def play_turn(self, treasure):
        action = self.choose_action(treasure)
        self.cards_left[action] = False
        return action

def train_rl_agent(episodes=1000):
    for episode in range(episodes):
        diamonds = [i for i in range(1, 13+1)]
        random.shuffle(diamonds)
        game = Game(diamonds)
        agent1 = RLAgent(1)
        agent2 = RLAgent(2)

        for t in range(13):
            treasure = game.diamonds[t]
            bid1 = agent1.play_turn(treasure)
            bid2 = agent2.play_turn(treasure)
            winner = game.turn(bid1, bid2, treasure)

            if winner == 1:
                agent1.update_q_table(treasure, bid1, treasure, game.diamonds[t+1] if t+1 < 13 else 0)
                agent2.update_q_table(treasure, bid2, -treasure, game.diamonds[t+1] if t+1 < 13 else 0)
            elif winner == 2:
                agent1.update_q_table(treasure, bid1, -treasure, game.diamonds[t+1] if t+1 < 13 else 0)
                agent2.update_q_table(treasure, bid2, treasure, game.diamonds[t+1] if t+1 < 13 else 0)
            else:
                agent1.update_q_table(treasure, bid1, 0, game.diamonds[t+1] if t+1 < 13 else 0)
                agent2.update_q_table(treasure, bid2, 0, game.diamonds[t+1] if t+1 < 13 else 0)

train_rl_agent()
'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.pygame_ai_player import PyGameAICombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[tuple(self.current_env_state)]
        return self.weapon


def run_random_episode(player, opponent):
    #Changing player healths to 50 to make the execution more feasible for virtual machine 
    #This still encapsulates all 3 moves the computer can make.
    #Would likely need 50000+ episodes for 100 health players to make an optimal policy, which takes way too long on VM.
    player.health = random.choice(range(10, 60, 10))
    opponent.health = random.choice(range(10, 60, 10))
    return run_episode(player, opponent)


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns

def run_episodes(n_episodes):
    ''' Run 'n_episodes' random episodes and return the action values for each state-action pair.
        Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
        Use the get_history_returns function to get the returns for each state-action pair in each episode.
        Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their returns.
        After all episodes have been run, calculate the average return for each state-action pair.
        Return the action values as a dictionary of dictionaries where the keys are states and 
            the values are dictionaries of actions and their values.
    '''
    player1 = PyGameAICombatPlayer("Random")
    player2 = PyGameComputerCombatPlayer("Computer")

    history = []

    for i in range(0, n_episodes):
    
        action_values = run_random_episode(player1, player2)

        history.append(get_history_returns(action_values))

    state = []

    uniqueState = []

    action_values = {}

    totalAvgZero = 0

    totalAvgOne = 0

    totalAvgTwo = 0

    numZero = 0
    numOne = 0
    numTwo = 0

    for episode in history:
        states = list(episode.keys())
        for i in states:
            state.append(i)

    for j in state:
        unique = True
        for t in uniqueState:
            if j == t:
                unique = False
        
        if unique == True:
            uniqueState.append(j)
    print("Unique States:")
    print(uniqueState)

    for key in uniqueState:
        action_values[key] = {0: 0, 1: 0, 2: 0}

    print("Blank action values:")
    print(action_values)

    for key in uniqueState:

        totalAvgZero = 0
        totalAvgOne = 0
        totalAvgTwo = 0

        numZero = 0
        numOne = 0
        numTwo = 0

        for episode in history:

            entries = episode.keys()

            for entry in entries:

                if entry == key:

                    actions = episode[entry].keys()

                    for action in actions:

                        if action == 0:
                            totalAvgZero += episode[entry][action]
                            numZero += 1
                        elif action == 1:
                            totalAvgOne += episode[entry][action]
                            numOne += 1
                        else:
                            totalAvgTwo += episode[entry][action]
                            numTwo += 1

        if numZero != 0:
            totalAvgZero = totalAvgZero / numZero
        else:
            totalAvgZero = 0

        if numOne != 0:
            totalAvgOne = totalAvgOne / numOne
        else:
            totalAvgOne = 0

        if numTwo != 0:
            totalAvgTwo = totalAvgOne / numTwo
        else:
            totalAvgTwo = 0

        action_values[key][0] = totalAvgZero
        action_values[key][1] = totalAvgOne
        action_values[key][2] = totalAvgTwo

    return action_values

def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    print(optimal_policy)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        #Changing player healths to 50 to make the execution more feasible for virtual machine.
        #This still encapsulates all 3 moves the computer can make.
        #Would likely need 50000+ episodes for 100 health players to make an optimal policy, which takes way too long on VM.
        player1.health = 50
        player2.health = 50
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(5000)
    optimal_policy = get_optimal_policy(action_values)
    print(optimal_policy)
    print(test_policy(optimal_policy))

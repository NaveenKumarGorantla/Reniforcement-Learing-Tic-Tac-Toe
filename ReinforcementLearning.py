from abc import ABC, abstractmethod
import collections
import numpy as np
import random as rand
rand.seed(0.1)
import matplotlib.pylab as plt
import timeit

class BaseLearner(ABC):
    def __init__(self, alpha, gamma, epsilon=0.1):
        # parameters
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # possible actionsAvailable
        self.actionsAvailable = self.get_possible_actions(None)

        # Initialize all a/s values to 0
        self.Q_StateAction_Values = self.Q_Val_Initialize()

        # record all rewards
        self.rewards = []

    # return moves available from current state
    def get_possible_actions(self, state):

        if state is None:
            possible_actions = [(j,i) for i in range(3) for j in range(3)]
        else:
            possible_actions = [a for a in self.actionsAvailable if state[a[0]*3 + a[1]] == '-']

        return possible_actions

    # initialize all state action pairs
    def Q_Val_Initialize(self):
        Q_StateAction_Values = {}
        for action in self.actionsAvailable:
            Q_StateAction_Values[action] = collections.defaultdict(int)
        return Q_StateAction_Values

    # initialize Eligibility trace
    def Initialize_EligibilityTrace(self):
        eligibilityTrace = {}
        for action in self.actionsAvailable:
            eligibilityTrace[action] = collections.defaultdict(int)
        return eligibilityTrace

    # to return the action with maximum value
    def getMaxStateAction(self, Q_StateAction_Values, state):
        max_value = -99999
        max_action = (0, 1)
        possible_actions = self.get_possible_actions(state)

        for action in possible_actions:

            value = Q_StateAction_Values[action][state]
            if value > max_value:
                max_value = value
                max_action = action

        return max_action

    # get epsilon greedy move
    def getEpsilonGreedyAction(self, state):
        possible_actions = self.get_possible_actions(state)
        rand = np.random.rand()
        # if rand number 0-1 is bigger or equal to epsilon then go with best policy
        if (rand < self.epsilon):
            action = possible_actions[np.random.choice(len(possible_actions))]
        else:
            action = self.getMaxStateAction(self.Q_StateAction_Values, state)
        return action

    # get e-greedy or greedy action
    def selectGreedyAction(self, state, epsilon=False):
        action = self.getEpsilonGreedyAction(state) \
            if epsilon else self.getMaxStateAction(self.Q_StateAction_Values, state)
        return action


'''
Q learning
'''


class Q_Learning(BaseLearner):
    def __init__(self, alpha, gamma, epsilon):
        super().__init__(alpha, gamma, epsilon)

    def update_StateActionValues(self, state, action, nextState, reward):
        
        if nextState is not None:
            possible_actions = super().get_possible_actions(nextState)
            if rand.random() < self.epsilon:
                nextAction = possible_actions[np.random.choice(len(possible_actions))]
                max_value = self.Q_StateAction_Values[nextAction][nextState]
            else:
                # get all the possible actions for the next state
                Q_options = [self.Q_StateAction_Values[action][nextState] for action in possible_actions]
                # update
                max_value = max(Q_options)
        else:
            max_value = 0

        self.Q_StateAction_Values[action][state] = self.Q_StateAction_Values[action][state] + self.alpha \
                                * (reward + self.gamma * max_value - self.Q_StateAction_Values[action][state])

        self.rewards.append(reward)


'''
Sarsa learning
'''


class Sarsa_Learning(BaseLearner):
    def __init__(self, alpha, gamma, epsilon):
        super().__init__(alpha, gamma, epsilon)

    def update_StateActionValues(self, state, action, nextState, reward):
        # checking whether it is final state
        if nextState is not None:

            # get the action for the next state
            nextAction = super().getEpsilonGreedyAction(nextState)
            # update
            next_action_value = self.Q_StateAction_Values[nextAction][nextState]
        else:  # when final state is arrived
            next_action_value = 0

        self.Q_StateAction_Values[action][state] = self.Q_StateAction_Values[action][state] + self.alpha \
                                * (reward + self.gamma * next_action_value - self.Q_StateAction_Values[action][state])

        self.rewards.append(reward)


'''
Sarsa lambda learning
'''


class Sarsa_lambda(BaseLearner):
    def __init__(self, alpha, gamma, epsilon):
        super().__init__(alpha, gamma, epsilon)
        self.Lambda = 0.6
        self.available_pos = [(i,j) for i in range(3) for j in range(3)]

    def update_StateActionValues(self, state, action, nextState, reward):
        # checking whether it is final state
        if nextState is not None:

            # get the action for the next state
            nextAction = super().getEpsilonGreedyAction(nextState)

            # update
            next_action_value = self.Q_StateAction_Values[nextAction][nextState]

        else:

            next_action_value = 0

        delta = reward + self.gamma * next_action_value - self.Q_StateAction_Values[action][state]

        self.eligibilityTrace[action][state] += 1

        for action1 in self.available_pos:
            for state1 in self.Q_StateAction_Values[action1]:
                self.Q_StateAction_Values[action1][state1] += self.alpha * delta * self.eligibilityTrace[action1][state1]
                self.eligibilityTrace[action1][state1] = self.gamma * self.Lambda * self.eligibilityTrace[action1][state1]
        self.rewards.append(reward)


class TicTacToeGame:
    def __init__(self, agent):
        self.agent = agent
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.final_reward = -99

    '''
    to occupy the position taken by agent
    '''

    def updateSmartAgentMove(self, action):
        self.board[action[0]][action[1]] = 'O'

    '''
    Returns the reward based on whether the computer wins or looses
    '''

    def gameStatus(self):
        for i in range(0, 3):
            # check rows
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] == 'O'):
                return 1
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] == 'X'):
                return -1
            # check cols
            if (self.board[0][i] == self.board[1][i] == self.board[2][i] == "O"):
                return 1
            if (self.board[0][i] == self.board[1][i] == self.board[2][i] == "X"):
                return -1

        # check downwards diagonal
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == "O"):
            return 1
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == "X"):
            return -1

        # check upwards diagonal
        if (self.board[2][0] == self.board[1][1] == self.board[0][2] == "O"):
            return 1
        if (self.board[2][0] == self.board[1][1] == self.board[0][2] == "X"):
            return -1

        return False

    '''
    to check whether the game is Tie
    '''

    def isGameTie(self):
        c = 0
        for row in self.board:
            for val in row:
                if val == '-':
                    c += 1
        if c == 0:
            return True
        return False

    '''
    moving to next state and next action
    '''

    def getNewStateAction(self, prev_state, prev_action):
        new_state = self.hash_board()
        new_action = self.agent.selectGreedyAction(new_state)
        self.agent.update_StateActionValues(prev_state, prev_action, new_state, 0)
        return new_state, new_action

    '''
    Places X at a random available location
    '''

    def getRandomAction(self):
        possibles = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    possibles += [(i, j)]
        action = possibles[rand.randint(0, len(possibles) - 1)]

        self.board[action[0]][action[1]] = 'X'

    '''
    When agent plays against computer, one will take action based on Q_StateAction_Values
    and other will take the random move
    '''

    def trainSmartAgent(self):
        if rand.random() < 0.5:
            self.getRandomAction()

        currentAction = None
        while True:
            if not currentAction:  # to take the action initially
                state = self.hash_board()
                currentAction = self.agent.selectGreedyAction(state)
            # agent move
            self.updateSmartAgentMove(currentAction)
            # check if game is completed
            if self.gameStatus():
                reward = self.gameStatus()
                self.final_reward = reward
                break;
            if self.isGameTie():
                reward = 0
                self.final_reward = reward
                break
            # the other agent will choose a random move
            self.getRandomAction()
            # check if game is completed
            if self.gameStatus():
                reward = self.gameStatus()
                self.final_reward = reward
                break;
            if self.isGameTie():
                reward = 0
                self.final_reward = reward
                break

            # updating the agent after every move
            state, currentAction = self.getNewStateAction(state, currentAction)

        # when final state is reached
        self.agent.update_StateActionValues(state, currentAction, None, reward)

    '''
    to ask the player to choose the move
    '''

    def getHumanAction(self):

        while True:
            pos = int(input("Please enter your position:- "))

            if pos not in range(1, 10):
                print("Number should be between 1 and 9")

            row = (pos - 1) // 3
            col = (pos - 1) % 3

            if self.board[row][col] != '-':
                print("position already filled")

            elif self.board[row][col] == '-':
                self.board[row][col] = 'X'
                break

    '''
    To play with Human
    '''

    def play_with_Human(self):
        self.display_raw_board()
        first = str(input("Do you want to first? y or n "))
        if first.upper() == 'Y':
            self.getHumanAction()
        elif first.upper() != 'N':
            print("Invalid option")
            self.play_with_Human()

        currentAction = None
        while True:
            if not currentAction:  # to initially take the step
                state = self.hash_board()
                currentAction = self.agent.selectGreedyAction(state)
            # agent move
            self.updateSmartAgentMove(currentAction)
            # check if game is completed
            if self.gameStatus():
                reward = self.gameStatus()
                break;
            if self.isGameTie():
                reward = 0
                break

            self.printBoard()
            print("Available positions to choose")
            hashboard = self.hash_board()
            
            availablePositions = [j+1 for j,i in enumerate(hashboard) if i=='-']  
            print(availablePositions)
            # asking for player move
            self.getHumanAction()
            # check if game is completed
            if self.gameStatus():
                reward = self.gameStatus()
                break;
            if self.isGameTie():
                reward = 0
                break
            # updating the agent after every move
            state, currentAction = self.getNewStateAction(state, currentAction)

        self.printBoard()  # print final board

        if reward == 0:
            print("It was a draw!")
        elif reward == -1:
            print("You won!")
        else:
            print("You lost!")

        # when final state is reached
        self.agent.update_StateActionValues(state, currentAction, None, reward)

    def startGame(self, training=False):
        # when  human wants to play
        if not training:
            start_time = timeit.default_timer()
            self.play_with_Human()
            stop_time = timeit.default_timer()
            print('time taken for Sarsas Algorithm with human: ', stop_time - start_time) 
        # to train the agent
        else:
            self.trainSmartAgent()

    '''
    to convert the board into single dimensional
    used in Q_StateAction_Values matrix
    '''

    def hash_board(self):
        boardPositions = ''
        for row in self.board:
            for value in row:
                boardPositions = boardPositions + value

        return boardPositions

    '''
    displaying the board with positions occupied
    '''

    def display_raw_board(self):
        print("The board positions are as follows")
        for i in range(3):
            print("-" + "----" * 3)
            x = "| "
            for j in range(3):
                x += str(3 * i + j + 1) + " | "
            print(x)
        print("-" + "----" * 3)

    '''
    displaying the board with positions occupied
    '''

    def printBoard(self):
        for row in self.board:
            print("-" + "----" * 3)
            x = "| "
            for val in row:
                if val == "-":
                    x += str(" ") + " | "
                else:
                    x += val + " | "

            print(x)
        print("-" + "----" * 3)


'''
Plots the rewards
'''

def plot_agent_reward(rewards):
    #plt.plot(np.cumsum(rewards))
    plt.plot(rewards)
    plt.title('# of episodes vs Q value for Q learning')
    plt.ylabel('Q value')
    plt.xlabel('# of Episodes')
    plt.show()

'''
to plot the winning percentage
'''
def plot_win_percent(rewards):
    #plt.plot(np.cumsum(rewards))
    draw_percen = []
    win_percen = []
    loss_percen = []
    draw = 0
    win = 0
    loss = 0
    for i, r in enumerate(rewards):
        if r == 0: draw+= 1
        elif r == 1: win += 1 
        else: loss += 1
        temp = i+1
        draw_percen.append(draw * 100 / temp)
        win_percen.append(win * 100 / temp)
        loss_percen.append(loss * 100 / temp)
        #print(temp, win)
    total = 100 / (i+1)
    print("The Q learning Smart Agent win percentage:-")
    print(f"win percentage:- {win * total}")
    print(f"loss percentage:- {loss * total}")
    print(f"draw percecentage:- {draw * total}")
    plt.plot(win_percen, label = 'smart player winning %')
    plt.plot(loss_percen, label = 'smart agent loss %')
    plt.plot(draw_percen, label = 'draw %')
    plt.xlabel('Number of episodes')
    plt.ylabel("rate")
    plt.title("percentage of winning of smart agent over number of episodes fo Q Learning")
    plt.legend()
    plt.show()

# Plotting cumulative discounted reward for different learning methods
def plotGraph_discountedReward(values):
    labels = [' Q Learning','Sarsa learning',' Sarsa lambda']
    for j,value in enumerate(values) :       
        sum1 = 0
        avg = []
        for i in range(len(value)):
            if(True):
                sum1 = sum1 + value[i]/(i+1)
                avg.append(sum1)
        plt.plot(avg,label = labels[j] )

    plt.title('Discounted cumulative reward vs. Episodes')
    plt.ylabel('Discounted cumulative reward')
    plt.xlabel('Episodes')
    plt.legend()
    plt.show()
    
# Plot cumulative discounted reward for a learning
def plot_discountedReward(values):
    cumulativeReward = []
    cumulativeSum = 0
    for i in range(len(values)):
        cumulativeSum += values[i]/(i+1)
        cumulativeReward.append(cumulativeSum)
    
    plt.plot(cumulativeReward)

    plt.title('Discounted cumulative reward vs. Episodes')
    plt.ylabel('Discounted cumulative reward')
    plt.xlabel('Episodes')
    #plt.legend()
    plt.show()



class playTicTacToe():
    def __init__(self, agentType, numOfEpisodes, alpha=0.3, gamma=0.9, epsilon=0.1):
        self.numOfEpisodes = numOfEpisodes
        self.q_value = []
        if agentType == "q":
            self.agent = Q_Learning(alpha, gamma, epsilon)
        elif agentType == "s":
            self.agent = Sarsa_Learning(alpha, gamma, epsilon)
        else:
            self.agent = Sarsa_lambda(alpha, gamma, epsilon)

    def humanAgent(self):
        while True:
            game = TicTacToeGame(self.agent)
            game.startGame()
            playAgain = input("Would you like to play again? ('y', 'n'): ")
            if playAgain == 'n':
                print("See you later!")
                break;

            print("\n Okay lets play again!")

    '''
    Teach agent - intelligence depends on number of games
    '''

    def trainSmartAgent(self):
        iteration = 0
        reward = []
        while iteration < self.numOfEpisodes:
            self.agent.eligibilityTrace = self.agent.Initialize_EligibilityTrace()
            game = TicTacToeGame(self.agent)
            game.startGame(training=True)
            iteration += 1
            self.q_value.append(self.agent.Q_StateAction_Values[(2, 2)]['OXXXXOOO-'])
            reward.append(game.final_reward)
            if iteration % 10000 == 0:
                print("Training round: " + str(iteration))
        #plot_win_percent(reward)
        #plot_discountedReward(reward)
        #plot_agent_reward(self.q_value)

'''
Gets Specification on training iterations and agent type from user
'''
def User_Input():
    print("Welcome to Tic-Tac-Toe")
    # get agentType
    
    while True:
        agentType = input("Please input Agent Type (qlearning or sarsa) 'q' or 's' or 'sl for sarsa(lambda)': ")
        if agentType == 'q':
            print('\n You choose to play with Q_StateAction_Values-learning!')
            break
        elif agentType == 's':
            print('\n You choose to play with SARSA!')
            break
        elif agentType == "sl":
            print('\n You choose to play with SARSA(lambda)!')
            break
        else:
            print("\n Invalid agent type: " + agentType)

    # getEpisodes
    if agentType == "sl":
        print("\nFor smart agent enter a value greater than or equal to ten thousand (10000): ")
    else:
        print("\nFor smart agent enter a value greater than or equal to forty thousand (40000): ")
    numOfEpisodes = int(input("Please enter the number of episodes you want to train agent: "))
    
    game = playTicTacToe(agentType, numOfEpisodes)
    game.trainSmartAgent()
    print("Done Training!")
    game.humanAgent()


if __name__ == "__main__":
    User_Input()

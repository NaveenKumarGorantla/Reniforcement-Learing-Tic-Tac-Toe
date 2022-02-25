import numpy as np
import pickle

Number_Rows = 3
Number_Columns = 3

class TicTacToe_Env:
    def __init__(self, player1, player2):
        self.GameBoard = np.zeros((Number_Rows, Number_Columns))
        self.player1 = player1
        self.player2 = player2
        self.isGameEnd = False
        self.Board_positions_1d_array = None
        # init player1 plays first
        self.player_ID = 1
    
    # get unique board positions array of current GameBoard TicTacToe_Env
    def get_Board_Positions(self):
        self.Board_positions_1d_array = str(self.GameBoard.reshape(Number_Columns*Number_Rows))
        return self.Board_positions_1d_array
    
    def Game_Result(self):
        # row check
        for i in range(Number_Rows):
            if sum(self.GameBoard[i, :]) == 3:
                self.isGameEnd = True
                return 1
            if sum(self.GameBoard[i, :]) == -3:
                self.isGameEnd = True
                return -1
        # column check
        for i in range(Number_Columns):
            if sum(self.GameBoard[:, i]) == 3:
                self.isGameEnd = True
                return 1
            if sum(self.GameBoard[:, i]) == -3:
                self.isGameEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.GameBoard[i, i] for i in range(Number_Columns)])
        diag_sum2 = sum([self.GameBoard[i, Number_Columns-i-1] for i in range(Number_Columns)])
        diag_sum = max(diag_sum1, diag_sum2)
        if diag_sum == 3:
            self.isGameEnd = True
            return 1
        elif diag_sum == -3:
            self.isGameEnd = True
            return -1
        
        # tie
        # no available positions
        if len(self.Unfilled_Positions()) == 0:
            self.isGameEnd = True
            return 0
        # not end
        self.isGameEnd = False
        return None
    
    def Unfilled_Positions(self):
        positions_available = []
        for i in range(Number_Rows):
            for j in range(Number_Columns):
                if self.GameBoard[i, j] == 0:
                    positions_available.append((i, j))  # need to be tuple
        return positions_available
    
    def Mark_Position_on_Board(self, position):
        self.GameBoard[position] = self.player_ID
        # switch to another RL_agent
        self.player_ID = -1 if self.player_ID == 1 else 1
    
    # only when game ends
    def Reward_Earned(self):
        result = self.Game_Result()
        # backpropagate reward
        if result == 1:
            self.player1.Update_State_Reward(1)
            self.player2.Update_State_Reward(0)
        elif result == -1:
            self.player1.Update_State_Reward(0)
            self.player2.Update_State_Reward(1)
        else:
            self.player1.Update_State_Reward(0.1)
            self.player2.Update_State_Reward(0.5)
    
    # GameBoard Reset_Game
    def Reset_Game(self):
        self.GameBoard = np.zeros((Number_Rows, Number_Columns))
        self.Board_positions_1d_array = None
        self.isGameEnd = False
        self.player_ID = 1
    
    def Play_Game(self, rounds=100):
        for i in range(rounds):
            if i%1000 == 0:
                print("Rounds {}".format(i))
            while not self.isGameEnd:
                # RL_agent 1
                positions = self.Unfilled_Positions()
                p1_action = self.player1.TakeAction(positions, self.GameBoard, self.player_ID)
                # take action and upate GameBoard TicTacToe_Env
                self.Mark_Position_on_Board(p1_action)
                board_hash = self.get_Board_Positions()
                self.player1.add_Env_State(board_hash)
                # check GameBoard status if it is end

                win = self.Game_Result()
                if win is not None:
                    # self.Display_Board()
                    # ended with player1 either win or draw
                    self.Reward_Earned()
                    self.player1.Reset_Game()
                    self.player2.Reset_Game()
                    self.Reset_Game()
                    break

                else:
                    # RL_agent 2
                    positions = self.Unfilled_Positions()
                    p2_action = self.player2.TakeAction(positions, self.GameBoard, self.player_ID)
                    self.Mark_Position_on_Board(p2_action)
                    board_hash = self.get_Board_Positions()
                    self.player2.add_Env_State(board_hash)
                    
                    win = self.Game_Result()
                    if win is not None:
                        # self.Display_Board()
                        # ended with player2 either win or draw
                        self.Reward_Earned()
                        self.player1.Reset_Game()
                        self.player2.Reset_Game()
                        self.Reset_Game()
                        break
    
    # Play_Game with human
    def Play_Game_Human(self):
        while not self.isGameEnd:
            # RL_agent 1
            positions = self.Unfilled_Positions()
            p1_action = self.player1.TakeAction(positions, self.GameBoard, self.player_ID)
            # take action and upate GameBoard TicTacToe_Env
            self.Mark_Position_on_Board(p1_action)
            self.Display_Board()
            # check GameBoard status if it is end
            win = self.Game_Result()
            if win is not None:
                if win == 1:
                    print(self.player1.name, "wins!")
                else:
                    print("tie!")
                self.Reset_Game()
                break

            else:
                # RL_agent 2
                positions = self.Unfilled_Positions()
                p2_action = self.player2.TakeAction(positions)

                self.Mark_Position_on_Board(p2_action)
                self.Display_Board()
                win = self.Game_Result()
                if win is not None:
                    if win == -1:
                        print(self.player2.name, "wins!")
                    else:
                        print("tie!")
                    self.Reset_Game()
                    break

    def Display_Board(self):
        # player1: x  player2: o
        for i in range(0, Number_Rows):
            print('-------------')
            out = '| '
            for j in range(0, Number_Columns):
                if self.GameBoard[i, j] == 1:
                    token = 'x'
                if self.GameBoard[i, j] == -1:
                    token = 'o'
                if self.GameBoard[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')    
        
        
        

class RL_agent:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_function_value = {}  # TicTacToe_Env -> value
    
    def get_Board_Positions(self, GameBoard):
        Board_positions_1d_array = str(GameBoard.reshape(Number_Columns*Number_Rows))
        return Board_positions_1d_array
    
    def TakeAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.get_Board_Positions(next_board)
                value = 0 if self.states_function_value.get(next_boardHash) is None else self.states_function_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action
    
    # append a hash TicTacToe_Env
    def add_Env_State(self, TicTacToe_Env):
        self.states.append(TicTacToe_Env)
    
    # at the end of game, backpropagate and update states value
    def Update_State_Reward(self, reward):
        for st in reversed(self.states):
            if self.states_function_value.get(st) is None:
                self.states_function_value[st] = 0
            self.states_function_value[st] += self.lr*(self.decay_gamma*reward - self.states_function_value[st])
            reward = self.states_function_value[st]
            
    def Reset_Game(self):
        self.states = []
        
    def save_Game_Policy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_function_value, fw)
        fw.close()

    def Load_Game_Policy(self, file):
        fr = open(file,'rb')
        self.states_function_value = pickle.load(fr)
        fr.close()
        
class HumanPlayer:
    def __init__(self, name):
        self.name = name 
    
    def TakeAction(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action
    
    # append a hash TicTacToe_Env
    def add_Env_State(self, TicTacToe_Env):
        pass
    
    # at the end of game, backpropagate and update states value
    def Update_State_Reward(self, reward):
        pass
            
    def Reset_Game(self):
        pass
    
    
player1 = RL_agent("player1")
player2 = RL_agent("player2")

st = TicTacToe_Env(player1, player2)
print("training...")
st.Play_Game(50000)



player1.save_Game_Policy()
player2.save_Game_Policy()

player1.Load_Game_Policy("policy_player1")

player1 = RL_agent("computer", exp_rate=0)
player1.Load_Game_Policy("policy_player1")

player2 = HumanPlayer("human")

st = TicTacToe_Env(player1, player2)
st.Play_Game_Human()
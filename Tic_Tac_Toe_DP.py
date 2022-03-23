# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 12:37:38 2022

@author: Bhavesh Kilaru, Naveen Kumar Gorantla
"""

import numpy as np
import timeit
class Tic_Tac_Toe():
    
    def __init__(self):
        #class variables variable 
        self.NumRows = 3
        self.NumCols = 3
        self.board = np.zeros((self.NumRows, self.NumCols))
        self.player_symbol = 0
        self.computer_symbol = 0
        self.is_end = False
        self.player_id = " "
        self.current_player = ""
        self.state_space = {}
        self.save_board_each_step = {}
    
    '''method to know who wants to go first'''
    def who_goes_first(self):
        
        first = str(input("Do you want to go First? Yes or No "))
        if first.upper() == "YES":
            self.current_player = "Human"
            return "Human"
        elif first.lower() == "no":
            self.current_player = "Computer"
            return "Computer"
    '''
    to assign symbols to the user
    the symbol 'x' will be represented as -1 
    where 'o' is represented as 1 on the board
    '''
    def assign_symbols(self):
        
        symbol = str(input("which symbol you prefer? 'X' or 'O' "))
        if(symbol.upper() == "X"):
            self.player_id = "X"
            self.player_symbol = -1
            self.computer_symbol = 1
        elif(symbol.upper() == "O"):
            self.player_id = "O"
            self.player_symbol = 1
            self.computer_symbol = -1
        else:
            print("please enter a valid symbol")
            self.assign_symbols()
        
    '''to display board along with positions occupied'''
    def display_board(self):
        for i in range(self.NumRows):
            print("-"+"----" * 3)
            x= "| "
            for j in range(self.NumCols):
                if self.board[i, j] == 1:
                    x += 'O' +" | "
                elif self.board[i, j] == -1:
                    x += 'X'+" | "
                else:
                    x += str(" ") + " | "
            print(x)
        print("-"+"----" * 3)
    
    '''to display the board along with values 
    that needs to be provided as input'''
    def display_raw_board(self):
        print("The board positions are as follows")
        for i in range(self.NumRows):
            print("-"+"----" * 3)
            x= "| "
            for j in range(self.NumCols):
                x += str(3 * i + j + 1) + " | "
            print(x)
        print("-"+"----" * 3)
       
    '''to represent board as a single dimensional array'''   
    def represent_board(self, board):
        board_list = []
        for  i in range(self.NumRows):
            for j in range(self.NumCols):
                board_list.append(board[i, j])
        return board_list
                
    '''to get all the positions that are unoccupied'''    
    def available_positions(self, board):
        positions = []
        for i in range(self.NumRows):
            for j in range(self.NumCols):
                if board[i, j] == 0:
                    positions.append((i,j))
        return positions
        
    '''to get the move from the user'''
    def ask_move(self):
        num = ""
        for (i,j) in self.available_positions(self.board):
            num+= str(i*3 + (j + 1))+ " "
            
        value = int(input(f"enter the position from the given:- {num}\n"))
        if value not in range(1,10):
            print("please enter a valid number")
            self.ask_move()
        elif ((value - 1)// 3, (value -1)% 3) not in self.available_positions(self.board):
            print("the position not available. please enter a another number")
            self.ask_move()
        return ((value - 1)// 3, (value -1)% 3)
    
    '''to fill a position with the correponding symbol
    'x' will be represented as -1 and 'o' will be represented as '1' '''
    def playMove(self, board, pos, symbol):
        board[pos] = symbol
        
    '''to check the winner'''
    def is_winner(self, board):
        
        #checking rows
        for i in range(self.NumRows):
            if(abs(sum(board[i])) == 3):
                #self.is_end = True
                return 1 if sum(board[i]) > 0 else -1
        #checking Cols
        for j in range(self.NumCols):
            if abs(sum(board[:, j])) == 3:
                #self.is_end = True
                return 1 if sum(board[:, j]) > 0 else -1
            
        #checking diagonals
        sum_diagonal1 = sum(board[i, self.NumRows-i-1] for i in range(self.NumRows))
        sum_diagonal2 = sum(board[i, i] for i in range(self.NumRows))
        if sum_diagonal1 == 3 or sum_diagonal2 == 3:
            return 1
        if sum_diagonal1 == -3 or sum_diagonal2 == -3:
            return -1
        
        if(len(self.available_positions(board)) == 0):
            return 0
        
        return None
    
    '''to print the winner
    This also prints when there is a tie '''
    def print_who_won(self):
        value = self.is_winner(self.board)
        if value is not None:
            if (value == 1 and self.player_id == "O") or (value == -1 and self.player_id == "X"):
               print("Kudos you won")
            elif value == 0:
               print("Hey it's a tie")
            else:
                print("I won")
    
    '''to determine who won the game'''   
    def determine_winner(self, board):
        value = self.is_winner(board)
        if value is not None:
            if (value == 1 and self.player_id == "O") or (value == -1 and self.player_id == "X"):
                return "Human"
            elif value == 0:
                return 0
            else:
                return "Computer"
    
    '''method to choose the best move  
    This uses min max algorithm'''
    def best_move(self):
        bestVal = -10
        bestMove = 0
        
        for i in self.available_positions(self.board):
            #temp_board = self.board
            #temp_board[i] = self.computer_symbol
            self.board[i] = self.computer_symbol
            
            moveVal = self.MinMax(self.board, 0, False, -10, 10)
            
            self.board[i] = 0
            
            if moveVal > bestVal:
                
                bestMove = i
                bestVal = moveVal
                
        return bestMove
     
    ''' Min-Max algorithm for dynamic programming
    The motive is to always maximize the reward'''
    def MinMax(self, board, depth, isMax, alpha, beta):
      	# Given a board and the computer's letter, determine where to move and return that move.
  
          if(self.determine_winner(board) == "Computer"):
              return 10
          if(self.determine_winner(board)  == "Human"):
              return -10
          if(self.determine_winner(board) == 0):
              return 0
          
          #when agent is maximixing the positive reward
          if isMax :
            
            best = -1000
            
            for i in self.available_positions(board):
                board[i] = self.computer_symbol
                best = max(best, self.MinMax(board, depth+1, not isMax, alpha, beta) - depth)
                alpha = max(alpha, best)
                board[i] = 0
                
                if alpha >= beta:
                    break
            return best
        
          #when agent is maximizing its negative reward
          else:
              best = 1000
              
              for i in self.available_positions(board):
                      board[i] = self.player_symbol
                      best = min(best, self.MinMax(board, depth+1, not isMax, alpha, beta) + depth)
                      beta = min(beta, best)
                      board[i] = 0
                      
                      if alpha >= beta:
                          break
              return best
    
    '''Method to play the game
    This should be called to play the game with user'''    
    def play(self):
        
        self.display_raw_board()
        self.who_goes_first()
        self.assign_symbols()
        iter = 0
        
        while not self.is_end:
            
            if self.current_player == "Human":
                
                print("It's your turn")
                pos = self.ask_move()
                self.playMove(self.board, pos, self.player_symbol)
                self.display_board()
                self.current_player = "Computer"
                
                if self.is_winner(self.board) is not None:
                    self.print_who_won()
                    self.is_end = True
                
            elif self.current_player == "Computer":
                comp_move = self.best_move()
                self.playMove(self.board, comp_move, self.computer_symbol)
                self.display_board()
                self.current_player = "Human"
                if self.is_winner(self.board) is not None:
                    self.print_who_won()
                    self.is_end = True
            
            self.save_board_each_step[str(iter)] = self.represent_board(self.board)
            iter += 1
                
            '''checking with the user whether he wants to play again'''    
            if self.is_end == True:
                play_again = str(input("Do you want to play again? Yes or No "))
                if play_again.lower() == "yes":
                    self.board = np.zeros((self.NumRows, self. NumCols))
                    self.is_end = False
                    self.play()
                else:
                    break
                
if __name__=="__main__":
    start_dp = timeit.default_timer()
    game = Tic_Tac_Toe()
    game.play()
    stop_dp = timeit.default_timer()
    print('The time taken by DP to play with Human: ', stop_dp - start_dp)
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 12:37:38 2022

@author: Naveen Kumar Gorantla
X - -1, O - 1
"""

import numpy as np
Nan = np.NaN
#import random as rand
class Tic_Tac_Toe():
    
    def __init__(self):
        self.NumRows = 3
        self.NumCols = 3
        self.board = np.zeros((self.NumRows, self.NumCols))
        self.player_symbol = 0
        self.computer_symbol = 0
        self.is_end = False
        self.player_id = " "
        
    def board_representation(self, board):
        board_map = []
        for row in range(self.NumRows):
            for col in range(self.NumCols):
                board_map.append(board[row, col])
        return board_map
    
    def position_is_empty(self, board, pos):
        return self.board[pos] == 0
    
    def who_goes_first(self):
        
        first = str(input("Do you want to go First? Yes or No\n"))
        if (first.upper() == "YES"):
            return "Human"
        else:
            return "Computer"
        
    def assign_symbols(self):
        
        symbol = str(input("which symbol you prefer? 'X' or 'O'\n"))
        if(symbol.upper() == "X"):
            self.player_id = "X"
            self.player_symbol = -1
            self.computer_symbol = 1
        elif(symbol.upper() == "O"):
            self.player_id = "O"
            self.player_symbol = 1
            self.computer_symbol = -1
        else:
            print("please enter a valid symbol\n")
            self.assign_symbols()
        
    
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
        
    def display_raw_board(self):
        for i in range(self.NumRows):
            print("-"+"----" * 3)
            x= "| "
            for j in range(self.NumCols):
                x += str(3 * i + j + 1) + " | "
            print(x)
        print("-"+"----" * 3)
        
    def available_positions(self, board):
        positions = []
        for i in range(self.NumRows):
            for j in range(self.NumCols):
                if board[i, j] == 0:
                    positions.append((i,j))
        return positions
        
        
    def ask_move(self):
        
        value = int(input("enter the position\n"))
        if value not in range(1, 10):
            print("please enter a valid number\n")
            self.ask_move()
        elif ((value - 1)// 3, (value -1)% 3) not in self.available_positions(self.board):
            print("the position not available. please enter a another number\n")
            self.ask_move()
        return ((value - 1)// 3, (value -1)% 3)
    
    def playMove(self, board, pos, symbol):
        board[pos] = symbol
        
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
        if sum_diagonal1 ==3 or sum_diagonal2 == 3:
            #self.is_end = True
            return 1
        if sum_diagonal1 == -3 or sum_diagonal2 == -3:
            #self.is_end = True
            return -1
        
        if(len(self.available_positions(board)) == 0):
            #self.game_ended = True
            return 0
        
        return None
    
    def print_who_won(self):
        value = self.is_winner(self.board)
        if value is not None:
            if (value == 1 and self.player_id == "O") or (value == -1 and self.player_id == "X"):
               print("Kudos you won")
               return "Human"
            elif value == 0:
               print("Hey it's a tie")
               return 0
            else:
                print("I won")
                return "Computer"
        
    def determine_winner(self, board):
        value = self.is_winner(board)
        if value is not None:
            if (value == 1 and self.player_id == "O") or (value == -1 and self.player_id == "X"):
                return "Human"
            elif value == 0:
                return 0
            else:
                return "Computer"
            
    def best_move(self):
        bestVal = -1000
        bestMove = -1
        
        for i in self.available_positions(self.board):
            #temp_board = self.board
            #temp_board[i] = self.computer_symbol
            self.board[i] = self.computer_symbol
            
            moveVal = self.MinMax(self.board, 0, False, -1000, 1000, self.computer_symbol)
            
            self.board[i] = 0
            
            if moveVal > bestVal:
                
                bestMove = i
                bestVal = moveVal
                
        return bestMove
        
    def MinMax(self, board, depth, isMax, alpha, beta, computerLetter):
      	# Given a board and the computer's letter, determine where to move and return that move.
  
          if self.determine_winner(board) == "Computer":
              return 10
          if self.determine_winner(board)  == "Human":
              return -10
          if self.determine_winner(board) == 0:
              return 0
          if isMax :
            best = -1000
            
            for i in self.available_positions(board):
                board[i] = self.computer_symbol
                best = max(best, self.MinMax(board, depth+1, not isMax, alpha, beta, computerLetter) - depth)
                alpha = max(alpha, best)
                board[i] = 0
                #print("computer options")
                #print(f"alpha : {alpha},beta : {beta},best : {best}")
                if alpha >= beta:
                    break
            return best
        
          else:
              best = 1000
              
              for i in self.available_positions(board):
                      board[i] = self.player_symbol
                      best = min(best, self.MinMax(board, depth+1, not isMax, alpha, beta, computerLetter) + depth)
                      beta = min(beta, best)
                      board[i] = 0
                      #print("player options\n")
                      #print(f"alpha : {alpha},beta : {beta},best : {best}\n")
                      if alpha >= beta:
                          break
              return best
        
    def play(self):
        
        self.display_raw_board()
        first = self.who_goes_first()
        print(first)
        self.assign_symbols()
        
        if first == "Human":
            pos = self.ask_move()
            self.playMove(self.board, pos, self.player_symbol)
            comp_move = self.best_move()
            self.playMove(self.board, comp_move, self.computer_symbol)
        elif first == "Computer":
            comp_move = self.best_move()
            self.playMove(self.board, comp_move, self.computer_symbol)
        
        self.display_board()
        
        while True:
            if self.is_end == True:
                play_again = str(input("Do you want to play again? Yes or No \n"))
                if play_again.lower() == "yes":
                    self.board = np.zeros((self.NumRows, self. NumCols))
                    self.is_end = False
                    self.play()
                else:
                    break
                
            pos = self.ask_move()
            self.playMove(self.board, pos, self.player_symbol)
            self.display_board()
            
            if self.is_winner(self.board):
                self.display_board()
                self.print_who_won()
                self.is_end = True
                
            
            comp_move = self.best_move()
            self.playMove(self.board, comp_move, self.computer_symbol)
            self.display_board()
            print("It's your turn")
            if self.is_winner(self.board):
                self.display_board()
                self.print_who_won()
                self.is_end = True

game = Tic_Tac_Toe()
game.play()
            
            
    
    
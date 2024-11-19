## Game of Pure Skill (GOPS)
## behaviour.py -- implements the game behaviour
## Kyle Sung
## 2024-11-19


import random
from getpass import getpass
import numpy as np



class Player:
    '''
    Encodes the behaviour for each of the players in the game
    '''

    def __init__(self, id):
        self.id = id
        self.cards_left = {
            i: True for i in range(1, 13+1)
        }
        self.points = 0
    
    def win_point(self, treasure):
        self.points += treasure



class Game:
    '''
    Encodes the game state (including the players, list of diamonds, and whether the previous turn was a tie (thus awarding more points)
    '''

    def __init__(self, diamonds):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.diamonds = diamonds
        self.tie = 0
    
    def turn(self, bid1, bid2, treasure):
        self.player1.cards_left[bid1] = False
        self.player2.cards_left[bid2] = False

        if bid1 > bid2:
            self.player1.win_point(treasure + self.tie)
            self.tie = 0
            winner = 1

        elif bid1 < bid2:
            self.player2.win_point(treasure + self.tie)
            self.tie = 0
            winner = 2

        elif bid1 == bid2:
            self.tie += treasure
            winner = 0
        
        return winner



def main():
    diamonds = [i for i in range(1, 13+1)]
    random.shuffle(diamonds)

    print(diamonds)
    game = Game(diamonds)

    for t in range(13):
        print(f"Begin Turn {t+1}. Treasure is: {game.diamonds[t]} + {game.tie}")
        
        error = True

        while error == True or game.player1.cards_left[bid1] == False:
            try:
                bid1 = int(getpass(f"Turn {t+1}. Player 1's Bid on Total Treasure {game.diamonds[t] + game.tie}: "))
                error = False
            except KeyboardInterrupt:
                exit()
            except (NameError, ValueError):
                error = True
                print("\n\t Input Error: Try again!")


        
        error = True

        while error == True or game.player1.cards_left[bid2] == False:
            try:
                bid2 = int(getpass(f"Turn {t+1}. Player 2's Bid on Total Treasure {game.diamonds[t] + game.tie}: "))
                error = False
            except KeyboardInterrupt:
                exit()
            except (NameError, ValueError):
                error = True
                print("\n\t Input Error: Try again!")

        w = game.turn(bid1, bid2, game.diamonds[t])

        if w != 0:
            print(f"Player {w} Wins {game.diamonds[t] + game.tie} with (1: {bid1}) against (2: {bid2})!")
        else:
            print(f"Draw! Both players bid {bid1}. Next turn")
        

        print(f"Standings:\n\tPlayer 1 has {game.player1.points} points\n\tPlayer 2 has {game.player2.points} points")

        print()


if __name__ == "__main__":
    main()

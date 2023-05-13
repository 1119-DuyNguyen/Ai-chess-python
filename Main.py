import chess
from Game import Game
game = Game(chess.Board(),chess.WHITE,chess.BLACK)
while(True):
    if(not game.startGame()) : break
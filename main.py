import threading
from tetris import Tetris

game = Tetris()
# Separate game thread permits interactive Python shell
# for object inspection 
game_thread = threading.Thread(target=game.run)
game_thread.start()

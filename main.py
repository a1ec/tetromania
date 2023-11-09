import threading
from state_machine import StateMachine

game = StateMachine()
# Separate game thread for object inspection in shell
game_thread = threading.Thread(target=game.run)

def main():
    game_thread.start()

if __name__ == "__main__":
    main()

 

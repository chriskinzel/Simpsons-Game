# Simpsons Game
This program is a text based game based on The Simpsons movie modelled as a 20x30 grid world.  
  
The world is loaded from a text file (player is prompted for path at startup).  
  
The goal of the game is to bring Homer from Alaska (top portion of the grid) back to the town of Springfield (near the bottom right). However if Homer takes too long to travel out of Alaska he will freeze and the player loses the game. Also if Homer moves into the water he drowns and the game is lost. Finally the tireless agents of the EPA will try to capture Homer and if that occurs the game is lost. The game will be run on a turn-by-turn basis. A turn elapses when: Homer moves or the player tries to move him (Homer ignores the command or the player tries to move Homer onto a building), Homer stays on the same square (direction 5), or the player toggles the debugging mode on or off. A turn won't pass if the player enters an erroneous value for the movement direction (10 or larger).  
  
The game continues until:     
  
1) The player has lost the game (Homer drowns, freezes or is captured).  
2) The player has won the game (Homer reaches Springfield).  
3) The player has quit the game.  

The game also supports a hidden debug mode (by entering a direction of -1) that will print out messages describing the internal state of the game such as how the EPA agent's are moving or whether or not Homer will be distracted.  
  
  
# Features
  
- Player can quit the game by entering '0' at the directional menu  
- Debugging mode implemented (debugs EPA agent movement and Homer distraction)  
  
- Homer can move in the 4 compass directions  
- Homer can get distracted  
- Game prevents Homer from moving onto occupied squares  
  
- EPA agents can move    
  
- Lose game condition implemented: Homer drowns if moved onto water  
- Lose game condition implemented: Homer can freeze in Alaska (Homer must remain in Alaska for at least 10 successive turns)  
- Lose game condition implemented: Homer captured by an EPA agent  
  
- Win game condition implemented: Homer reaching Springfield  
  
# Running
    python3 assignment4.py

#
#       Assignment #4
# -------------------------
#
# Version: 3.3
#
# Name: Chris Kinzel
# ID: 10160447
# Section: 09
#
#
# Description:
# ---------------
# This program is a text based game based on The Simpsons movie modeled as a
# 20x30 grid world.
#
# The world is loaded from a text file (player is prompted for path at startup).
#
# The goal of the game is to bring Homer from Alaska (top portion of the grid)
# back to the town of Springfield (near the bottom right). However if Homer
# takes too long to travel out of Alaska he will freeze and the player loses
# the game. Also if Homer moves into the water he drowns and the game is lost.
# Finally the tireless agents of the EPA will try to capture Homer and if that
# occurs the game is lost. The game will be run on a turn-by-turn basis. A turn
# elapses when: Homer moves or the player tries to move him
# (Homer ignores the command or the player tries to move Homer onto a building),
# Homer stays on the same square (direction 5), or the player toggles the
# debugging mode on or off. A turn won't pass if the player enters an erroneous
# value for the movement direction (10 or larger).
#
# The game continues until:
#
# 1) The player has lost the game (Homer drowns, freezes or is captured).
# 2) The player has won the game (Homer reaches Springfield).
# 3) The player has quit the game.
#
# The game also supports a hidden debug mode (by entering a direction of -1)
# that will print out messages describing the internal state of the game such
# as how the EPA agent's are moving or whether or not Homer will be distracted.
#
#
# Features:
# ---------------
# - Displays introduction
# - Displays conclusion
# - Displays directional menu
#
# - Loads start positions from file
#
# - Error message is displayed if player tries to move Homer in the 4 inter-cardinal directions
# - Error message is displayed if player tries to enter a value higher than 9 for the direction
#
# - Player can quit the game by entering '0' at the directional menu
# - Debugging mode implemented (debugs EPA agent movement and Homer distraction)
#
# - Homer can move in the 4 compass directions
# - Homer can get distracted
# - Game prevents Homer from moving onto occupied squares
#
# - EPA agents can move
#
# - Lose game condition implemented: Homer drowns if moved onto water
# - Lose game condition implemented: Homer can freeze in Alaska (Homer must remain in Alaska for at least 10 successive turns)
# - Lose game condition implemented: Homer captured by an EPA agent
#
# - Win game condition implemented: Homer reaching Springfield
#
#
# Limitations:
# ---------------
# - Can only handle 20x30 grid (will crash for smaller size and produce unexpected behavior with larger sizes)
# - No error checking done on inputted file (i.e. size check, content check)
#
#

import random

#####################
#  GLOBAL CONSTANTS
#####################

WORLD_ROWS = 20
WORLD_COLUMNS = 30

EMPTY_TILE = " "
BUILDING_TILE = "#"
HOMER_TILE = "H"
EPA_AGENT_TILE = "E"
SPRINF_TILE = "S"
WATER_TILE = "~"

NORTH = 8
EAST  = 6
STAY  = 5
WEST  = 4
SOUTH = 2
QUIT  = 0

END_CODE_WIN    =  1
END_CODE_EXIT   =  2
END_CODE_DROWN  =  3
END_CODE_EPA    =  4
END_CODE_FROZEN =  5

VALID_MOVES = (-1,QUIT,SOUTH,WEST,STAY,EAST,NORTH)
COORD_DIRECTION_MAP = ((1,WEST,7),(NORTH,STAY,SOUTH),(3,EAST,9)) # Address COORD_DIRECTION_MAP[∆x+1][∆y+1]

# Debugging off by default enter movement direction of -1 to enable
debug = False

# Global variable to store last direction for repeat moves (faster movement than typing #'s all the time)
lastDirection = STAY # THIS IS CUBERSOME TO DO WITHOUT A GLOBAL 

# Finds Homer position in the world given as argument 'world'.
#
# Returns a tuple containing the x and y coordinates of Homer in the world.
def getHomerPosition(world):
    for x in range(WORLD_COLUMNS):
        for y in range(WORLD_ROWS):
            if(world[y][x] == HOMER_TILE):
                return (x,y)

# Finds all EPA agent positions in the world given as argument 'world'.
#
# Returns a list containing a set of tuples of the form (x,y)/(c,r) where
#         the agents are located in the world.
def getAgentPositions(world):
    agentPositions = []
    
    for x in range(WORLD_COLUMNS):
        for y in range(WORLD_ROWS):
            if(world[y][x] == EPA_AGENT_TILE):
                agentPositions.append( (x,y) )

    return agentPositions
            

# Loads game world as 20x30 list from a text file.
# Requires a path to a text file to load as the argument 'filename'
#
# Returns a 2D character list (20x30) of the populated game world from the
#         text file.
def loadWorld(filename):
    try:
        worldFile = open(filename, "r")
    except IOError:
        print("\nERROR: World file not found '%s'. Program will now terminate. Goodbye!" %filename, end="\n\n")
        exit()

    world = []
    
    for line in worldFile:
        world.append(list(line.rstrip("\n\r")))

    worldFile.close()

    return world

# Prompts user for cardinal direction to move Homer as well as handling
# invalid input.
#
# Returns an integer indicating the direction the player wishes Homer to move.
def getUserInput():
    global lastDirection # Reference global lastDirection
    
    print("""
Movement options, the numbers correspond to the 4 compass directions (5 to not move). Or enter 0 to quit the game.

  8
4 5 6
  2""", end="\n\n")

    inputString = ""
    direction = 0
    printError = True
    
    while printError:
        printError = False
        
        inputString = input("Enter movement direction (Blank repeats last move):")

        try:
            direction = int(inputString)
        except ValueError:
            if(len(inputString) == 0):
                return lastDirection

            printError = True

        if(not direction in VALID_MOVES):
            printError = True

        if(printError):
            if(direction > 9):
                print("\n%i is not a valid direction." %direction, end="\n\n")
            else:
                print("\nHomer doesn't know how to move that way.", end="\n\n")

    lastDirection = direction
    
    return direction

# Prints a specific conclusion message according to the argument 'state' and
# then exits the program.
#
# Returns none (exits program)
def conclusionMessage(state):
    print("\n\n CONCLUSION:", end="\n ")
    print("-----------------------------------------------------------------------------", end="\n ")
    
    if(state == END_CODE_WIN):
        print("You've brought Homer back to Springfield. You win!", end="\n\n\n")
    elif(state == END_CODE_FROZEN):
        print("Homer spent too much time in Alaska and froze. You lose!", end="\n\n\n")
    elif(state == END_CODE_DROWN):
        print("Homer fell into the water and drowned. You lose!", end="\n\n\n")
    elif(state == END_CODE_EPA):
        print("Homer was captured by the EPA. You lose!", end="\n\n\n")
    elif(state == END_CODE_EXIT):
        print("Qutting game... Bye bye!", end="\n\n\n")

    exit()

# Updates all EPA agents position in the world given as argument 'world'. Also
# requires argument 'articTime' for world rendering (when Homer is caught).
# Detects if any of the EPA agents have caught Homer (adjacent).
#
# Returns None
def updateEPAAgents(world, articTime):
    agentPositions = getAgentPositions(world)
    homerPos       = getHomerPosition(world)

    # Add newline to output if debugging for clarity
    if(debug):
        print()

    for agentPos in agentPositions:
        # Build list of all possible moves
        moveSet = [(agentPos[0], agentPos[1], STAY)] # Have to use this ugly setup thanks to debug requirement
        
        for x in range(-1, 2):
            for y in range(-1, 2):
                proposedX = agentPos[0] + x
                proposedY = agentPos[1] + y

                # Calculate dummy direction variable since it's required in
                # assignment description for debug
                direction = COORD_DIRECTION_MAP[x+1][y+1]

                # Wrap world
                if(proposedX < 0):
                    proposedX = WORLD_COLUMNS-1
                elif (proposedX >= WORLD_COLUMNS):
                    proposedX = 0
        
                if(proposedY < 0):
                    proposedY = WORLD_ROWS-1
                elif (proposedY >= WORLD_ROWS):
                    proposedY = 0

                if(world[proposedY][proposedX] == EMPTY_TILE):
                    moveSet.append( (proposedX, proposedY, direction) )

        # Randomly select a move and update world
        newPos = random.choice(moveSet)

        # Debug message for EPA Agent movement
        if(debug):
            print("<<< Agent direction: %i, Agent source (r/c): (%i/%i), Agent destination (r/c): (%i/%i) >>>" %(newPos[2], agentPos[1], agentPos[0], newPos[1], newPos[0]) )
        
        world[agentPos[1]][agentPos[0]] = EMPTY_TILE
        world[newPos[1]][newPos[0]] = EPA_AGENT_TILE

        # Check if this agent caught homer
        if( (homerPos[0] - newPos[0])**2 + (homerPos[1] - newPos[1])**2 <= 2):
            renderWorld(world, articTime)            
            conclusionMessage(END_CODE_EPA)

    # Add newline to output if debugging for clarity
    if(debug):
        print()
        

# Updates Homer's position in the world given as argument 'world' relative to
# the direction passed as the argument 'direction'.
#
# Returns None
def updateHomer(world, direction):
    # Check if homer is distracted
    distractionChance = random.random()

    # Debug message for homer's distraction
    if(debug and direction != 5):
        print("\n<<< Number randomly generated = %f >>>" %distractionChance)
        print("<<< Number < 0.25, Homer is distracted >>>")
        print("<<< Number >= 0.25, Homer follows player's movement instructions >>>")

        if(distractionChance < 0.25):
            print("<<< Homer becomes distracted and refuses to move >>>")
        else:
            print("<<< Homer follows the player's movement instructions >>>")

        print()
    
    if(distractionChance < 0.25 and direction != 5):
        print("\n*** HOMER BECOMES DISTRACTED AND REFUSES TO MOVE ***")
        return
    
    homerPos = getHomerPosition(world)

    proposedX = homerPos[0]
    proposedY = homerPos[1]

    if(direction == SOUTH):
        proposedY += 1
    elif (direction == NORTH):
        proposedY -= 1

    if(direction == WEST):
        proposedX -= 1
    elif (direction == EAST):
        proposedX += 1

    # Wrap world
    if(proposedX < 0):
        proposedX = WORLD_COLUMNS-1
    elif (proposedX >= WORLD_COLUMNS):
        proposedX = 0
        
    if(proposedY < 0):
        proposedY = WORLD_ROWS-1
    elif (proposedY >= WORLD_ROWS):
        proposedY = 0
        
    if(world[proposedY][proposedX] == EMPTY_TILE):
        world[homerPos[1]][homerPos[0]] = EMPTY_TILE
        world[proposedY][proposedX] = HOMER_TILE
    elif(world[proposedY][proposedX] == SPRINF_TILE):
        conclusionMessage(END_CODE_WIN)
    elif(world[proposedY][proposedX] == WATER_TILE):
        conclusionMessage(END_CODE_DROWN)
    elif(world[proposedY][proposedX] != HOMER_TILE):
        print("\nHomer can't walk through walls.")
        

# Updates the world given as argument 'world' and the 'articTime' argument according
# to the game rules and the given 'direction' argument.
#
# Returns the total elasped articTime
def updateWorld(world, articTime, direction):
    global debug # Reference global debug flag
    
    if(direction == QUIT): # Quit program
        conclusionMessage(END_CODE_EXIT)
    
    if(direction == -1): # Toggle debug mode
        debug = not debug
        print("\n<<< DEBUG MODE %s -- TURN NOT COUNTED >>>" %("ENABLED" * int(debug) + "DISABLED" * int(not debug) ) )
        
        return articTime
    
    updateHomer(world, direction)
    updateEPAAgents(world, articTime)

    # Update artic time
    homerPos = getHomerPosition(world)

    if(homerPos[1] < 6):
        articTime += 1
    else:
        articTime = 0

    if(articTime >= 10): # Homer has frozen
        renderWorld(world, articTime)
        conclusionMessage(END_CODE_FROZEN)

    return articTime
        

# Renders the game world given as argument 'world' as a 20x30 grid as well as
# displaying the time spent and remaining in Alaska denoted by argument 'articTime'
#
# Returns nothing.
def renderWorld(world, articTime):
    print()
    print("Time spent in Alaska %i." %articTime)
    print("Remaining turns unitl Homer freezes in Alaska %i." %(10-articTime), end="\n\n")
    
    for i in range (WORLD_ROWS):
        print("".join(world[i]))


######################
# PROGRAM ENTRY POINT 
######################

def main():
    # Give introductory message explaining game
    print("""
  INTRODUCTION:
 -------------------------------------------------------------------------------
 The goal of the game is to bring Homer from Alaska (top six rows of the grid)
 back to the town of Springfield (near the bottom right). However if Homer takes
 too long to travel out of Alaska he will freeze and you lose the game
 (10 turns). Also if Homer moves into the water he drowns and the game is lost.
 Finally the tireless agents of the EPA will try to capture Homer and if that
 occurs the game is lost.

 The game is rendered as a 20x30 character grid as follows:

 Character:               Representation:
 ----------    -----------------------------------------
     H         Homer Simpson (controlled by the player)

     #         A building (cannot be entered)

     E         Agents of the EPA (controlled by the computer)

     ~         Water (Homer can enter, EPA agents cannot)

     S         The town of Springfield (Homer can enter, EPA agents cannot)
     

 The game is divided into a series of turns during which the player can input a  cardinal direction for Homer to move (N = 8, W = 4, E = 6, S = 2), passing a
 turn is also possible by entering an input of 5. You can quit the game at any
 time by entering a value of 0 for the direction input.""", end="\n\n")

    # Get world file path from user
    print(" This program requires a file containing the starting state of the game world.", end="\n\n\n")
    worldFilePath = input("Enter path to world file (relative to your current working directory):")

    # Initialization
    articTime = 0
    world = loadWorld(worldFilePath)

    # Work loop
    while True:
        renderWorld(world, articTime)
        direction = getUserInput()
        articTime = updateWorld(world, articTime, direction)
    
main()

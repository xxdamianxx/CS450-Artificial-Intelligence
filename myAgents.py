"""
@author Pedro Damian Sanchez Jr

@created 02/04/2024
"""
from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent
from util import manhattanDistance


class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor
        # Add anything else you think you need here

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """

        # Your code
        if (ghost.isScared()):
            return Directions.STOP
        # Compare pacman position to ghost position: first retrieve pacman position from pacstate (pacman)
        # second retrieve ghost position from ghoststate (ghost)
        pacPos = pacman.getPosition()
        ghostPos = ghost.getPosition()


        # Check if the column or row of the pacman and ghost match, if one does: dangerous = True
        # also check if manhattanDistance(pacPos, ghostPos) <= dist
        # And ghost is not scared

        if ((manhattanDistance(pacPos, ghostPos) <= dist) or (((pacPos[0] == ghostPos[0]) or (pacPos[1] == ghostPos[1])) and (manhattanDistance(pacPos, ghostPos) <= dist))):
            #DANGEROUS

            # If the columns are the same then check if pacman is to the north or south. To do this, check if pacman row is > or < ghost row
            # Else >, go north. If <, go south.
            # If the rows are the same, check if pacman column is > or < ghost column, if > then east, if < then west

            if (pacPos[0] == ghostPos[0]):
                if (pacPos[1] > ghostPos[1]):
                    return Directions.NORTH
                else:
                    return Directions.SOUTH

            # Else if the rows are the same then check if pacman is to the east or west. To do this, check if pacman columns is > or < ghost columns
            # Else >, go east. If <, go west.
            # If the columns are the same, check if pacman row is > or < ghost row, if > then north, if < then south
            elif (pacPos[1] == ghostPos[1]):
                if (pacPos[0] > ghostPos[0]):
                    return Directions.EAST
                else:
                    return Directions.WEST
        else:
            return Directions.STOP
        return

    
    def getAction(self, state):
        """
        state - GameState
        
        Fill in appropriate documentation
        """
        direction = ""

        # get pacman state
        pacState = state.getPacmanState()
        # get ghost states
        allGhostsStates = state.getGhostStates()

        # PacMan reacts to nearby ghosts
        for ghostState in allGhostsStates:
            direction = self.inDanger(pacState, ghostState)

            # Restricts movement of PacMan
            legalActions = state.getLegalPacmanActions()

            reversed = Actions.reverseDirection(direction)

            if not direction == Directions.STOP:
                #DANGER
                if direction in legalActions:
                    return direction
                else:
                    # Find the direction pacman is facing, try left then right then whatever is possible
                    # if north, try west. If south, try east. If east, try north. If west, try south
                    pacDirection = pacState.getDirection()
                    if (pacDirection == Directions.NORTH) and (Directions.WEST in legalActions):
                        return Directions.WEST
                    elif (pacDirection == Directions.NORTH) and (Directions.EAST in legalActions):
                        return Directions.EAST
                    elif (pacDirection == Directions.NORTH) and (reversed in legalActions):
                        return reversed

                    if (pacDirection == Directions.SOUTH) and (Directions.EAST in legalActions):
                        return Directions.EAST
                    elif (pacDirection == Directions.SOUTH) and (Directions.WEST in legalActions):
                        return Directions.WEST

                    if (pacDirection == Directions.EAST) and (Directions.NORTH in legalActions):
                        return Directions.NORTH
                    elif (pacDirection == Directions.EAST) and (Directions.SOUTH in legalActions):
                        return Directions.SOUTH

                    if (pacDirection == Directions.WEST) and (Directions.SOUTH in legalActions):
                        return Directions.SOUTH
                    elif (pacDirection == Directions.WEST) and (Directions.NORTH in legalActions):
                        return Directions.NORTH

                    if (reversed in legalActions):
                        return reversed

                    return Directions.STOP

        # Use left turn agent
        leftAgent = LeftTurnAgent()
        return leftAgent.getAction(state)
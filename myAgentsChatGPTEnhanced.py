"""
@author Pedro Damian Sanchez Jr with ChatGPT

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
        # Add any necessary initialization here

    def inDanger(self, pacman, ghost, dist=3):
        """
        Determines if Pacman is in danger from a ghost.
        
        Args:
            pacman (AgentState): State of the Pacman agent.
            ghost (AgentState): State of the ghost agent.
            dist (int, optional): Distance threshold for considering Pacman in danger. Defaults to 3.

        Returns:
            str: Direction of danger if Pacman is in danger, else Directions.STOP.
        """
        if ghost.isScared():
            return Directions.STOP
        
        pacPos = pacman.getPosition()
        ghostPos = ghost.getPosition()

        if manhattanDistance(pacPos, ghostPos) <= dist and (pacPos[0] == ghostPos[0] or pacPos[1] == ghostPos[1]):
            # Pacman is in danger
            if pacPos[0] == ghostPos[0]:
                return Directions.NORTH if pacPos[1] > ghostPos[1] else Directions.SOUTH
            elif pacPos[1] == ghostPos[1]:
                return Directions.EAST if pacPos[0] > ghostPos[0] else Directions.WEST
        else:
            return Directions.STOP

    def getAction(self, state):
        """
        Determines the next action for Pacman based on the current game state.
        
        Args:
            state (GameState): Current game state.

        Returns:
            str: Next action for Pacman.
        """
        pacState = state.getPacmanState()
        allGhostsStates = state.getGhostStates()
        
        for ghostState in allGhostsStates:
            direction = self.inDanger(pacState, ghostState)
            legalActions = state.getLegalPacmanActions()
            reversed_direction = Actions.reverseDirection(direction)

            if direction != Directions.STOP:
                if direction in legalActions:
                    return direction
                else:
                    pacDirection = pacState.getDirection()
                    if pacDirection == Directions.NORTH:
                        if Directions.WEST in legalActions:
                            return Directions.WEST
                        elif Directions.EAST in legalActions:
                            return Directions.EAST
                    elif pacDirection == Directions.SOUTH:
                        if Directions.EAST in legalActions:
                            return Directions.EAST
                        elif Directions.WEST in legalActions:
                            return Directions.WEST
                    elif pacDirection == Directions.EAST:
                        if Directions.NORTH in legalActions:
                            return Directions.NORTH
                        elif Directions.SOUTH in legalActions:
                            return Directions.SOUTH
                    elif pacDirection == Directions.WEST:
                        if Directions.SOUTH in legalActions:
                            return Directions.SOUTH
                        elif Directions.NORTH in legalActions:
                            return Directions.NORTH
                    
                    if reversed_direction in legalActions:
                        return reversed_direction

                    return Directions.STOP
        
        # If Pacman is not in danger, use LeftTurnAgent's behavior
        leftAgent = LeftTurnAgent()
        return leftAgent.getAction(state)

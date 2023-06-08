# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        #Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()

        currentFood = currentGameState.getFood().asList()
        # 10 points for every food you eat
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        newCapsule = successorGameState.getCapsules()
        # 200 points for every ghost you eat
        # but no point for capsule

        # For Ghost
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # Position of ghost do not change regardless of your state
        # because you can't predict the future
        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        # Count down from 40 moves
        ghostStartPos = [ghostState.start.getPosition() for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"

        score = successorGameState.getScore()

        # if next position of agent is the same as the food then +10
        if newPos in currentFood:
            score += 10.0 

        # Check food
        if len(newFood) > 0 :
            closestFood = min([manhattanDistance(newPos, newFoodItem) for newFoodItem in newFood])
            score += 10.0 / closestFood   - 10.0 * len(newFood)     

        # Check Capsule        
        if len(newCapsule) > 0:
            closestCapsule = min([manhattanDistance(newPos, capsule) for capsule in newCapsule])
            if closestCapsule < 5:
                score += 10.0 / closestCapsule - 50.0 *  len(newCapsule)
            else:
                score += 1.0 / closestCapsule - 50.0 *  len(newCapsule)

        # Check Ghost 
        numberGhost = len(newGhostStates)
        ghostTimerActivated = 0

        for i in newScaredTimes:
            if i>0:
                ghostTimerActivated +=1

        for ghostIndex in range(numberGhost):
            timerGhost = newScaredTimes[ghostIndex]
            distantAgentGhost = manhattanDistance(newPos, ghostPositions[ghostIndex])
            if timerGhost == 0:
                if distantAgentGhost < 2:
                    score -= 75.0 
            else:
                if distantAgentGhost < 2:
                    score += 10.0 / distantAgentGhost - 1.0 * ghostTimerActivated

        return score 
        
def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # GET ACTIONS
        action  = self.minimax(gameState)  
        return action[0]
        util.raiseNotDefined()

    def minimax(self, gameState, depth = 0, agentIndex = 0):
        # RESTART INDEF OF THE AGENT TO ZERO WHEN IS GREATHER THAN AVAILABLE AGENTS
        if agentIndex >= gameState.getNumAgents() :
            agentIndex = 0 
            depth +=1
        
        # if TERMINAL_TEST(state) then return UTILITY(state)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        # MAZIMIZE WHEN IS PACMAN
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)
        # MINIMIZE WHEN IS GHOST
        else:
            return self.minValue(gameState, depth, agentIndex)
        
    def maxValue(self, gameState, depth = 0, agentIndex = 0):
        # DEFINE v = -inf
        v = ["", float('-inf')]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.minimax(succesor, depth , agentIndex + 1) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # v = MAX(v, MIN_VALUE(RESULT(s, a))
            if scoreV > v[1]:
                v = [action, scoreV]
        return v

    def minValue(self, gameState, depth = 0, agentIndex = 0):
        # DEFINE v = inf
        v = ["", float('inf')]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.minimax(succesor, depth , agentIndex + 1) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # v = MIN(v, MAX_VALUE(RESULT(s, a))
            if scoreV < v[1]:
                v = [action, scoreV]
        return v

  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action  = self.alphaBethaSearch(gameState)  
        return action[0]
        util.raiseNotDefined()

    def alphaBethaSearch(self, gameState, depth = 0, agentIndex = 0, alpha = float('-inf'), beta = float('inf')):
        # RESTART INDEX OF THE AGENT TO ZERO WHEN IS GREATHER THAN AVAILABLE AGENTS
        if agentIndex >= gameState.getNumAgents() :
            agentIndex = 0 
            depth +=1

        # if TERMINAL-TEST(state) then return UTILITY(state)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        # MAZIMIZE WHEN IS PACMAN
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex, alpha, beta)
        # MINIMIZE WHEN IS GHOST
        else:
            return self.minValue(gameState, depth, agentIndex, alpha, beta)
        
    def maxValue(self, gameState, depth, agentIndex, alpha, beta):
        # DEFINE v = -inf
        v = ["", float('-inf')]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.alphaBethaSearch(succesor, depth , agentIndex + 1, alpha, beta) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # v = MAX(v, MIN_VALUE(RESULT(s, a))
            if scoreV > v[1]:
                v = [action, scoreV]
            # if v > beta then return v
            if scoreV > beta:
                return v
            # alpha = MAX(alpha, v)
            alpha = max(alpha, scoreV)
        return v

    def minValue(self, gameState, depth, agentIndex, alpha, beta):
        # DEFINE v = inf
        v = ["", float('inf')]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.alphaBethaSearch(succesor, depth , agentIndex + 1, alpha, beta) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # v = MIN(v, MAX_VALUE(RESULT(s, a))
            if scoreV < v[1]:
                v = [action, scoreV]
            # if v < alpha then return v
            if scoreV < alpha:
                return v
            # beta = MIN(beta, v)
            beta = min(beta, scoreV)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        action  = self.expectimaxSearch(gameState)  
        return action[0]
        util.raiseNotDefined()

    def expectimaxSearch(self, gameState, depth = 0, agentIndex = 0):
        # RESTART INDEX OF THE AGENT TO ZERO WHEN IS GREATHER THAN AVAILABLE AGENTS 
        if agentIndex >= gameState.getNumAgents() :
            agentIndex = 0 
            depth +=1

        # if TERMINAL-TEST(state) then return UTILITY(state)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        # MAZIMIZE WHEN IS PACMAN
        elif agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)
        # MINIMIZE WHEN IS GHOST
        else:
            return self.expectedValue(gameState, depth, agentIndex)


    def maxValue(self, gameState, depth = 0, agentIndex = 0):
        # DEFINE v = -inf
        v = ["", float('-inf')]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.expectimaxSearch(succesor, depth , agentIndex + 1) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # v = MAX(v, MIN_VALUE(RESULT(s, a))
            if scoreV > v[1]:
                v = [action, scoreV]
        return v
    
    def expectedValue(self, gameState, depth = 0, agentIndex = 0):
        # DEFINE v = 0
        v = ["", 0]
        # GET POSSIBLE ACTIONS FROM AGENT
        legalActions = gameState.getLegalActions(agentIndex)
        # IF NOT ACTIONS RETURN SCORE
        if not legalActions:
            return self.evaluationFunction(gameState)
        # PROBABILITY OF EACH POSSIBLE OUTCOME
        probability = 1.0 / len(legalActions)
        # VERIFY EACH ACTION
        for action in legalActions:
            succesor = gameState.generateSuccessor(agentIndex, action)
            score =  self.expectimaxSearch(succesor, depth , agentIndex + 1) 
            # scoreV = score[1] if type(score) is list else score
            try:
                scoreV = score[1]
            except (TypeError, IndexError):
                # HANDLE THE CASE WHERE SCORE IS NOT A LIST
                scoreV = score 
            # ACCUMULATES THE CONTRIBUTION OF EACH OUTCOME TO THE OVERALL EXPECTED VALUE OF THE MOVE
            expectedValue = v[1] + scoreV  * probability 
            v = [action, expectedValue]
        return v
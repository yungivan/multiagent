# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"

        
        foodpos = newFood.asList()
        foodcount = successorGameState.getNumFood()

        #min distance from food
        minfooddist = 99999999
        for coord in foodpos:
          fooddist =  manhattanDistance(newPos, coord)
          if minfooddist > fooddist:
            minfooddist = fooddist

        #min distance from ghost
        minghost = 999999
        for ghost in newGhostStates: 
          ghostdist = manhattanDistance(newPos, ghost.getPosition())
          minghost = min(minghost, ghostdist)
        if minghost <2:
            return float('-inf')

        return successorGameState.getScore() + 10/(minfooddist+1) - 100 * foodcount
        #return score 

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
     
        self.pcount = gameState.getNumAgents()
        if self.depth == 0:
            return float('inf')
        
        #optmove = Directions.STOP
        v = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(agentIndex)
        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp =  self.minhelper(successor, 1, self.depth)
            if tmp >= v:
                optmove = move
                v = tmp
        return optmove

    def maxhelper(self, gameState, depth):
        
        if depth == 0:
            return self.evaluationFunction(gameState)

        maxnum = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(gameState)

        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp = self.minhelper(successor, 1,depth)
            #print tmp
            maxnum = max(tmp, maxnum)
            
        return maxnum

    def minhelper(self, gameState, agentIndex, depth):
        
        if depth ==0:
            return self.evaluationFunction(gameState)

        minnum = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        if actions == []:
            return self.evaluationFunction(gameState)
    
        for move in actions:
            successor = gameState.generateSuccessor(agentIndex, move)
            if agentIndex == self.pcount -1 :
                tmp = self.maxhelper(successor, depth-1)
            else: 
                tmp = self.minhelper(successor, agentIndex+1, depth)
            minnum = min(minnum, tmp)
        return minnum


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf')
        beta = float('inf')
        self.pcount = gameState.getNumAgents()
        if self.depth == 0:
            return float('inf')
        
        optmove = Directions.STOP
        v = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(agentIndex)
        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp =  self.minhelper(successor, 1, self.depth, alpha, beta)
            if tmp >= v:
                optmove = move
                v = tmp
            if v > beta:
                return v
            alpha = max(alpha, v)
        return optmove

    def maxhelper(self, gameState, depth, alpha, beta):
        
        if depth == 0:
            return self.evaluationFunction(gameState)

        maxnum = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(gameState)

        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp = self.minhelper(successor, 1,depth, alpha, beta)
            #print tmp
            maxnum = max(tmp, maxnum)
            if maxnum > beta: 
                return maxnum
            alpha = max(alpha, maxnum)
            
        return maxnum

    def minhelper(self, gameState, agentIndex, depth, alpha, beta):
        
        if depth ==0:
            return self.evaluationFunction(gameState)

        minnum = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        if actions == []:
            return self.evaluationFunction(gameState)
    
        for move in actions:
            successor = gameState.generateSuccessor(agentIndex, move)
            if agentIndex == self.pcount -1 :
                tmp = self.maxhelper(successor, depth-1, alpha, beta)
            else: 
                tmp = self.minhelper(successor, agentIndex+1, depth, alpha, beta)
            minnum = min(minnum, tmp)
            if minnum < alpha:
                return minnum
            beta = min(beta, minnum)
        return minnum

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.pcount = gameState.getNumAgents()
        if self.depth == 0:
            return float('inf')
        
        optmove = Directions.STOP
        v = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(agentIndex)
        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp =  self.minhelper(successor, 1, self.depth)
            if tmp > v:
                optmove = move
                v = tmp
        return optmove

    def maxhelper(self, gameState, depth):
        
        if depth == 0:
            return self.evaluationFunction(gameState)

        maxnum = float('-inf')
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(gameState)
        #sumnum = 0
        #countnum = 0
        for move in actions: 
            successor = gameState.generateSuccessor(0, move)
            tmp = self.minhelper(successor, 1,depth)
            #sumnum += tmp
            #countnum += 1
            #print tmp
            maxnum = max(tmp, maxnum)
            
        return maxnum
        #sumnum/countnum

    def minhelper(self, gameState, agentIndex, depth):
        
        if depth ==0:
            return self.evaluationFunction(gameState)

        minnum = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        if actions == []:
            return self.evaluationFunction(gameState)
        sumnum = 0
        countnum = 0
        for move in actions:
            successor = gameState.generateSuccessor(agentIndex, move)
            if agentIndex == self.pcount -1 :
                tmp = self.maxhelper(successor, depth-1)
            else: 
                tmp = self.minhelper(successor, agentIndex+1, depth)
            sumnum += tmp
            countnum += 1
            #minnum = min(minnum, tmp)

        return sumnum/countnum

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #action = currentGameState.getLegalActions(0)
    #if action == []:
    #    return float('-inf')
     
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #print newGhostStates
    #print "~~~~~~~~~"
    #print newScaredTimes
    #print "~~~"
    #if action == Directions.STOP: 
    #    return -9999
    
    newScaredTimesAndPositions = [(ghostState.scaredTimer, ghostState.getPosition()) for ghostState in newGhostStates]
    distance = float('inf')
    for ghostState in newScaredTimesAndPositions:
        ghostTime, ghostPosition = ghostState
        newDistance = manhattanDistance(ghostPosition, newPos)
        if distance > newDistance:
            isScared = ghostTime
            distance = newDistance

    if isScared > 2 and distance < 10:
        scareghost = 200 + distance

    elif distance <= 2:
        scareghost =  -20
    elif distance <= 1:
        scareghost =  -100
    else:
        scareghost = distance

        

    foodpos = newFood.asList()
    foodcount = currentGameState.getNumFood()

    #min distance from food
    minfooddist = float('inf')
    for coord in foodpos:
        fooddist =  manhattanDistance(newPos, coord)
        minfooddist = min(minfooddist, fooddist)

    #min distance from ghost
    minghost = float('inf')
    for ghost in newGhostStates: 
        ghostdist = manhattanDistance(newPos, ghost.getPosition())
        minghost = min(minghost, ghostdist)
    if minghost <2:
        return float('-inf')

    return currentGameState.getScore() + 10/(minfooddist+1) - 100 * foodcount + scareghost/10

# Abbreviation
better = betterEvaluationFunction

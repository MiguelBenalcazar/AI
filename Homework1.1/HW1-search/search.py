# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST

    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
   
    # initialize the frontier using the initial state of problem
    frontier = util.Stack()
  
    # create start node (state, action, cost)
    node = (problem.getStartState(), [],0)
    frontier.push(node)
    # initialize the explored set to be empty
    explored = []
   
    frontier, _, action =  graphSearch(problem, frontier, explored)
    print(f"DFS COST OF ACTIONS: {problem.getCostOfActions(action)}")
    return action 
    util.raiseNotDefined() 


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # initialize the frontier using the initial state of problem
    frontier = util.Queue()

    # create start node (state, action, cost)
    node = (problem.getStartState(), [], 0)
    frontier.push(node)
    # initialize the explored set to be empty
    explored = []

    _, _, action =  graphSearch(problem, frontier, explored)
    print(f"BFS COST OF ACTIONS: {problem.getCostOfActions(action)}")
    return action 
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # node ←a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    node = (problem.getStartState(), [],0)
    initPriority = 0
    # initialize the frontier using the initial state of problem
    frontier = util.PriorityQueue()
    # create start node (state, action, cost)
    frontier.push(node, initPriority)
    # explored ← an empty set
    explored = []

    _, _, action= costGraphSearch(problem, frontier, explored)
    print(f"UFS COST OF ACTIONS: {problem.getCostOfActions(action)}")
    return action 
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # node ←a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    node = (problem.getStartState(), [],0)
    initPriority = 0
    # initialize the frontier using the initial state of problem
    frontier = util.PriorityQueue()
    # create start node (state, action, cost)
    frontier.push(node, initPriority)
    # explored ← an empty set
    explored = []

    _, _, action = costAStartSearch(problem, frontier, explored, heuristic)
    return action

    util.raiseNotDefined()


def graphSearch(problem, frontier, explored):
    """
        Recursive function created to help breath first search and depth first search 
        Inputs:
            problem
            frontier: set of nodes that have been discovered but not yet explored
            explored: save node already explored
        Outputs:
            frontier:
            explored:
            action: list of actions to take
    """
    action = []
    # if the frontier is empty then return failure
    if not frontier.isEmpty():
        # choose a leaf node and remove it from the frontier
        state, action, cost = frontier.pop()

        #if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        if problem.isGoalState(state):
            return frontier, explored, action     

        #add the node to the explored 
        if state not in explored:
            explored.append(state)
            # get all of the successors from current state
            successors = problem.getSuccessors(state)
            # Explore all of the succesors and add them to the frontier
            for node_successor in successors:  
                # if node in successor has not been explored  add to frontier 
                if node_successor[0] not in explored:
                    frontier.push((node_successor[0], action + [node_successor[1]], cost + node_successor[2]))
        
        # recursive function until finding the goal
        frontier, explored, action = graphSearch(problem, frontier, explored)
        
    return frontier, explored, action


def costGraphSearch(problem, frontier, explored):
    action = []
    # if EMPTY?(frontier ) then return failure
    if not frontier.isEmpty():
        # frontier.print()
        #node ← POP(frontier ) /* chooses the lowest-cost node in frontier */
        state, action, cost  = frontier.pop()
    
        # if state not in explored:
        #     explored.append(state)

        # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        if problem.isGoalState(state):
            return frontier, explored, action
     
        if state not in explored:
            explored.append(state)
            successors = problem.getSuccessors(state)

            for i in successors:  
                path = action + [i[1]]
                item = (i[0], path , cost + i[2])
                priority = problem.getCostOfActions(path) #cost + i[2] 

                existInFrontier = searchHeap(i[0], frontier)
        
                # if succesors are not in the explored
                if i[0] not in explored:
                    # if not exist in the frontier and not priority queue
                    if  not existInFrontier:
                        frontier.push(item, priority)
                    # If item already in priority queue with higher priority, update its priority and rebuild the heap.
                    elif existInFrontier:
                        #if new priority is less than the previous priority
                        if (priority < priorityHeap(i[0], frontier)):
                            frontier.update(item, priority)

        frontier, explored, action = costGraphSearch(problem, frontier, explored)
    return frontier, explored, action

def costAStartSearch(problem, frontier, explored, heuristic):
    action = []
    
    # if EMPTY?(frontier ) then return failure
    if not frontier.isEmpty():
        #node ← POP(frontier ) /* chooses the lowest-cost node in frontier */
        state, action, cost  = frontier.pop()
 
        #if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        if problem.isGoalState(state):
            return frontier, explored, action

        if state not in explored:
            explored.append(state)
            successors = problem.getSuccessors(state)
            for i in successors:  
                newAction = action + [i[1]]
                item = (i[0], newAction , cost + i[2])
                priority = problem.getCostOfActions(newAction) #cost + i[2] 


                # If item not in priority queue, do the same thing as self.push.
                if  i[0] not in explored:
                    # g(n) cost to reach the node
                    g_n = priority
                    # h(n) cost from node to the goal
                    h_n = heuristic(i[0], problem)
                    # estimated cost of the cheapest solution through n
                    f_n = g_n + h_n

                    frontier.push(item, f_n)
  
        frontier, explored, action = costAStartSearch(problem, frontier, explored, heuristic)
    return frontier, explored, action


def searchHeap(state, frontier):
    for stateFrontier in frontier.heap:
        if state == stateFrontier[2][0]:
            return True
    return False


def priorityHeap(state, frontier):
    for stateFrontier in frontier.heap:
        if state == stateFrontier[2][0]:
            return stateFrontier[2][2] 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
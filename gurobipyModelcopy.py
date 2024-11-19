from math import ceil
import os
import time
import gurobipy as gp
from gurobipy import GRB
import json as js
from random import shuffle
from src.cascadeGrouping import CascadeGrouping

bestSolution_callBack = 0

class DinnerWithFriendsSolver:
    def __init__(self):
        self.model = None  # Gurobi model
        self.meets = None  # Decision variables for pupils meeting each other at least once
        self.meetsAtE = None  # Decision variables for pupils meeting each other at a specific event
        self.meetsAtEInG = None  # Decision variables for pupils meeting in a group at a specific event
        self.isInGroupAtE = None  # Decision variables for pupils being in a group at a specific event
        self.groupInUse = None  # Decision variables for whether a group is in use at an event
        self.visits = None  # Decision variables for whether one pupil visits another at an event
        self.isHost = None  # Decision variables for whether a pupil is hosting an event
        self.Events = []  # Events range
        self.Kids = []  # List of all children
        self.Groups = []  # Groups range
        self.Pairs = []  # List of all distinct pairs of children
        self.Girls = []  # List of girls
        self.Boys = []  # List of boys
        self.numKids = 0  # Number of kids
        self.numGroups = 0  # Number of groups at each event
        self.minNumGuests = 0  # Minimum number of guests in a group
        self.maxNumGuests = 0  # Maximum number of guests in a group
        self.numOfEvents = 0  # Number of events
        self.timeLimit = 0  # Time limit for solving

    def readData(self, filenameOrDict: str):
        # Read the data from the JSON file
        if isinstance(filenameOrDict,str):
            if os.path.exists(filenameOrDict):
                with open(filenameOrDict) as f:
                    classData = js.load(f)
            else:
                raise FileNotFoundError("Can't locate the given path")

        elif isinstance(filenameOrDict,dict):
                classData = filenameOrDict
        else:
            raise ValueError('MakeSure the input is either a dict or a correctly specified path')
        
        assert sorted(classData.keys()) == ['maxNumGuests','minNumGuests','n_boys','n_girls','numOfEvents'], "Given input does not contain the necessary keys, ['minNumGuests','maxNumGuests','n_boys','n_girls','numOfEvents']"

        self.Girls = [f'girl_{i}' for i in range(classData['n_girls'])]
        self.Boys = [f'boy_{i}' for i in range(classData['n_boys'])]
        # if classData['shuffle_kids']:
        #     shuffle(self.Girls)
        #     shuffle(self.Boys)
        self.Kids = self.Girls + self.Boys
        self.numKids = len(self.Kids)
        self.minNumGuests = classData['minNumGuests']
        self.maxNumGuests = classData['maxNumGuests']
        self.numOfEvents = classData['numOfEvents']
        self.numGroups = ceil(self.numKids / self.minNumGuests)
        self.Events = range(0, self.numOfEvents)
        self.Groups = range(0, self.numGroups)
        # self.timeLimit = classData['timeLimitInSeconds']
        self.constructionHeuristic = CascadeGrouping(len(self.Girls),len(self.Boys),self.minNumGuests,self.maxNumGuests)
        # Create all unique pairs of kids
        for i in range(0, len(self.Kids) - 1):
            for j in range(i + 1, len(self.Kids)):
                self.Pairs.append((self.Kids[i], self.Kids[j]))
        self.initializeModel()
        self.createVariables()
        self.buildModel()

    def initializeModel(self):
        # Initialize the Gurobi model
        self.model = gp.Model("DinnerWithFriends")
        #self.model.setParam('TimeLimit', self.timeLimit)

    def createVariables(self):
        # Decision variables for pupils meeting at least once during the events
        self.meets = self.model.addVars(self.Pairs, vtype=GRB.BINARY, name="meets")
        # Decision variables for pupils meeting in a group at a specific event
        self.meetsInG = self.model.addVars(self.Pairs, self.Groups, vtype=GRB.BINARY, name="meetsInG")
        # Decision variables for pupils being in a group at a specific event
        self.isInGroup = self.model.addVars(self.Kids, self.Groups, vtype=GRB.BINARY, name="isInGroup")
        # Decision variables for whether a group is in use at an event
        self.groupInUse = self.model.addVars(self.Groups, vtype=GRB.BINARY, name="groupInUse")
        # Decision Variable for if group has both gender types
        self.groupsGotBothGenders = self.model.addVars(self.Groups,vtype=GRB.BINARY, name="groupsGotBothGenders")

    def buildModel(self):
        self.constraintCount = 0
        # Maximize the total number of distinct pair meetings
        self.model.setObjective(gp.quicksum(self.groupsGotBothGenders[g] for g in self.Groups), GRB.MAXIMIZE)

        # Constraints ensuring each kid attends exactly one group at each event
        for i in self.Kids:
                self.model.addConstr(gp.quicksum(self.isInGroup[i, g] for g in self.Groups) == 1)
                self.constraintCount += 1

        # Constraints for group size limits (if a group is in use)
        for g in self.Groups:
                self.model.addConstr(gp.quicksum(self.isInGroup[i, g] for i in self.Kids) <= self.maxNumGuests * self.groupInUse[g])
                self.model.addConstr(gp.quicksum(self.isInGroup[i, g] for i in self.Kids) >= self.minNumGuests * self.groupInUse[g])
                self.constraintCount += 2

        # Gender balance constraints
        for g in self.Groups:
                for j in self.Girls:
                    self.model.addConstr(gp.quicksum(self.isInGroup[i, g] for i in self.Girls) >= 2 * self.isInGroup[j, g])
                    self.constraintCount += 1
                for j in self.Boys:
                    self.model.addConstr(gp.quicksum(self.isInGroup[i, g] for i in self.Boys) >= 2 * self.isInGroup[j, g])
                    self.constraintCount += 1

        for g in self.Groups:
             self.model.addConstr(self.groupsGotBothGenders[g] <= gp.quicksum(self.isInGroup[j,g] for j in self.Girls))
             self.model.addConstr(self.groupsGotBothGenders[g] <= gp.quicksum(self.isInGroup[j,g] for j in self.Boys))
             

        # Linearize the relationship for pupils meeting in a group at an event
        for (i, j) in self.Pairs:
            for g in self.Groups:
                    self.model.addConstr(self.meetsInG[i, j, g] <= self.isInGroup[i, g])
                    self.model.addConstr(self.meetsInG[i, j, g] <= self.isInGroup[j, g])
                    self.model.addConstr(self.meetsInG[i, j, g] >= self.isInGroup[i, g] + self.isInGroup[j, g] - 1)
                    self.constraintCount += 3

        # Pupils meet if they are in the same group at any event
        for (i, j) in self.Pairs:
                self.model.addConstr(self.meets[i, j] == gp.quicksum(self.meetsInG[i, j, g] for g in self.Groups))
                self.constraintCount += 1


        # Enforce group usage constraints (groups must be used consecutively, starting from group 0)
        for g in range(1, self.numGroups):
                self.model.addConstr(self.groupInUse[g] <= self.groupInUse[g - 1])
                self.constraintCount += 1

        self.model.update()


    def solveModel(self,timeLimit):


        objValues = []
        runTimes = []

        def callback(model,where):

            global bestSolution_callBack

            if where == GRB.Callback.MIPSOL:

                currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)

                if currentValue > bestSolution_callBack:

                    runTime = time.time()
                    objValues.append(currentValue)
                    runTimes.append(runTime)
                    bestSolution_callBack = currentValue 

        self.model.setParam("TimeLimit", timeLimit)
        self.model.optimize(callback)

        return objValues,runTimes
if __name__ == '__main__':
    dwf = DinnerWithFriendsSolver()
    dwf.readData('exampleData.json')
    dwf.solveModel()
    pass
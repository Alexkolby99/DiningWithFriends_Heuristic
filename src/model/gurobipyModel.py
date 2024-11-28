from math import ceil
import os
import time
import gurobipy as gp
from gurobipy import GRB
import json as js
from random import shuffle
from src.cascadeGrouping import CascadeGrouping

class DinnerWithFriendsSolver:
    def __init__(self,modelFactory):
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
        self.modelFactory = modelFactory
        self.bestSolutionCallback = 0

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
        # Decision variables for pupils meeting at a specific event
        self.meetsAtE = self.model.addVars(self.Pairs, self.Events, vtype=GRB.BINARY, name="meetsAtE")
        # Decision variables for pupils meeting in a group at a specific event
        self.meetsAtEInG = self.model.addVars(self.Pairs, self.Groups, self.Events, vtype=GRB.BINARY, name="meetsAtEInG")
        # Decision variables for pupils being in a group at a specific event
        self.isInGroupAtE = self.model.addVars(self.Kids, self.Groups, self.Events, vtype=GRB.BINARY, name="isInGroupAtE")
        # Decision variables for whether a group is in use at an event
        self.groupInUse = self.model.addVars(self.Groups, self.Events, vtype=GRB.BINARY, name="groupInUse")
        # Decision variables for one pupil visiting another at an event
        self.visits = self.model.addVars(self.Kids, self.Kids, self.Events, vtype=GRB.BINARY, name="visits")
        # Decision variables for whether a pupil is hosting an event
        self.isHost = self.model.addVars(self.Kids, self.Events, vtype=GRB.BINARY, name="isHost")


    def setFeasibleSolution(self):

        events = self.constructionHeuristic.constructSolution(self.numOfEvents)
        if events is not None:

            self.model.update() 
            for v in self.model.getVars():
                v.start = 0

            for eventNum,sol in enumerate(events[1:]):
                for gNum,g in enumerate(sol.groups):
                    host = self.Kids[g.host.identifier]
                    if len(g.members) != 0:
                        self.groupInUse[gNum,eventNum].start = 1
                    
                    self.isHost[host,eventNum].start = 1

                    for m1 in g.members:
                        if self.Kids[m1.identifier] != host:
                            self.visits[host,self.Kids[m1.identifier],eventNum].start = 1
                        self.isInGroupAtE[self.Kids[m1.identifier],gNum,eventNum].start = 1
                        for m2 in g.members:
                            if m1 != m2:
                                kid1 = self.Kids[min(m1.identifier,m2.identifier)]
                                kid2 = self.Kids[max(m1.identifier,m2.identifier)]
                                self.meets[kid1,kid2].start = 1
                                self.meetsAtE[kid1,kid2,eventNum].start = 1
                                self.meetsAtEInG[kid1,kid2,gNum,eventNum].start = 1
            self.model.update()            

    def buildModel(self):
        # Maximize the total number of distinct pair meetings
        self.modelFactory.setObjectiveFunction(self)
        self.modelFactory.setAdditionalConstraints(self)


        for pair in self.Pairs:
            i,j = pair
            for e in self.Events:
                if e != len(self.Events)-1:
                    self.model.addConstr(self.meetsAtE[i,j,e] + self.meetsAtE[i,j,e+1] <= 1)

        # Constraints ensuring each kid attends exactly one group at each event
        for i in self.Kids:
            for e in self.Events:
                self.model.addConstr(gp.quicksum(self.isInGroupAtE[i, g, e] for g in self.Groups) == 1)
                

        # Constraints for group size limits (if a group is in use)
        for g in self.Groups:
            for e in self.Events:
                self.model.addConstr(gp.quicksum(self.isInGroupAtE[i, g, e] for i in self.Kids) <= self.maxNumGuests * self.groupInUse[g, e])
                self.model.addConstr(gp.quicksum(self.isInGroupAtE[i, g, e] for i in self.Kids) >= self.minNumGuests * self.groupInUse[g, e])
                

        # Gender balance constraints
        for g in self.Groups:
            for e in self.Events:
                for j in self.Girls:
                    self.model.addConstr(gp.quicksum(self.isInGroupAtE[i, g, e] for i in self.Girls) >= 2 * self.isInGroupAtE[j, g, e])
                    
                for j in self.Boys:
                    self.model.addConstr(gp.quicksum(self.isInGroupAtE[i, g, e] for i in self.Boys) >= 2 * self.isInGroupAtE[j, g, e])
                    

        # Linearize the relationship for pupils meeting in a group at an event
        for (i, j) in self.Pairs:
            for g in self.Groups:
                for e in self.Events:
                    self.model.addConstr(self.meetsAtEInG[i, j, g, e] <= self.isInGroupAtE[i, g, e])
                    self.model.addConstr(self.meetsAtEInG[i, j, g, e] <= self.isInGroupAtE[j, g, e])
                    self.model.addConstr(self.meetsAtEInG[i, j, g, e] >= self.isInGroupAtE[i, g, e] + self.isInGroupAtE[j, g, e] - 1)
                    

        # Pupils meet if they are in the same group at any event
        for (i, j) in self.Pairs:
            for e in self.Events:
                self.model.addConstr(self.meetsAtE[i, j, e] == gp.quicksum(self.meetsAtEInG[i, j, g, e] for g in self.Groups))
                

        # A pair meets at least once across all events if they meet in at least one event
        for (i, j) in self.Pairs:
            self.model.addConstr(self.meets[i, j] <= gp.quicksum(self.meetsAtE[i, j, e] for e in self.Events))
            

        # Enforce group usage constraints (groups must be used consecutively, starting from group 0)
        for g in range(1, self.numGroups):
            for e in self.Events:
                self.model.addConstr(self.groupInUse[g, e] <= self.groupInUse[g - 1, e])
                

        # Ensure each kid is a host at least once across all events
        for i in self.Kids:
            self.model.addConstr(gp.quicksum(self.isHost[i, e] for e in self.Events) >= 0)
            

        # Ensure the number of hosts equals the number of groups in use at each event
        for e in self.Events:
            self.model.addConstr(gp.quicksum(self.isHost[i, e] for i in self.Kids) == gp.quicksum(self.groupInUse[g, e] for g in self.Groups))
            

        # Ensure if i and j in the same group they cannot both be host
        for (i,j) in self.Pairs:
            for e in self.Events:
                self.model.addConstr(self.isHost[i,e] + self.isHost[j,e] <= 2 - self.meetsAtE[i,j,e])
                

        # Ensure no pupil is a host in consecutive events
        for i in self.Kids:
            for e in range(1, self.numOfEvents):
                self.model.addConstr(self.isHost[i, e - 1] + self.isHost[i, e] <= 1)
                

        # Linearize the visits relation
        for e in self.Events:
            for i in self.Kids:
                for j in self.Kids:
                    self.model.addConstr(self.visits[i, j, e] <= self.isHost[i, e])
                    
                    if (i,j) in self.Pairs:
                        self.model.addConstr(self.visits[i, j, e] <= self.meetsAtE[i, j, e])
                        self.model.addConstr(self.visits[i, j, e] >= self.isHost[i, e] + self.meetsAtE[i, j, e] - 1)
                        
                    elif (j,i) in self.Pairs:
                        self.model.addConstr(self.visits[i, j, e] <= self.meetsAtE[j, i, e])
                        self.model.addConstr(self.visits[i, j, e] >= self.isHost[i, e] + self.meetsAtE[j, i, e] - 1)
                        
        self.model.update()

    def solveModel(self,timeLimit):


        objValues = []
        runTimes = []

        def callback(model,where):

            if where == GRB.Callback.MIPSOL:

                currentValue = model.cbGet(GRB.Callback.MIPSOL_OBJ)

                if currentValue > self.bestSolutionCallback:

                    runTime = time.time()
                    objValues.append(currentValue)
                    runTimes.append(runTime)
                    self.bestSolutionCallback = currentValue 

        self.model.setParam("TimeLimit", timeLimit)
        self.model.optimize(callback)

        return objValues,runTimes
if __name__ == '__main__':
    dwf = DinnerWithFriendsSolver()
    dwf.readData('exampleData.json')
    dwf.solveModel()
    pass
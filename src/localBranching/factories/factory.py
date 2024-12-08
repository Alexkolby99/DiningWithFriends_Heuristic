from typing import Dict
from src.localBranching._interfaces import Brancher_base, Terminate_base
from src.localBranching.branchingStrategies import StandardVariableBranching
from src.localBranching.branchingStrategies.kStrategies import PercentageK, FixedK
from src.localBranching.terminateStrategies import InstantTerminater, ImprovementBoundTerminater
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.model.factories import MaximizeMeetsFactory


class Factory:

    def __init__(self,data: Dict,trackData: bool) -> None:
        self.model = DinnerWithFriendsSolver(MaximizeMeetsFactory())
        self.model.readData(data)
        self.model.model.setParam("DegenMoves", 1) # avoid these moves since takes a while without much benefits when not solving for optimality
        #self.model.model.setParam('MIPFocus', 1) # focus on finding good feasible solutions rather than optimality
        self.model.setFeasibleSolution()
        self.variable = ['meets','meets','meets']
        numberOfTotalMeets = self.findBound(data['n_girls']+data['n_boys'],
                                            data['maxNumGuests'],
                                            data['minNumGuests'],
                                            data['numOfEvents'])
        self.kStrategies = [PercentageK(0.05),PercentageK(0.15),PercentageK(0.25)] #0.5 and 0.6 works
        self.trackData = trackData
        self.maxTimePerVariable = 30 # only does something if multiple variables are used
        self.changing = False
        self.improvementPercentage = 0.02
        self.instantThreshhold = 30

    def getBrancher(self) -> Brancher_base:
        
        return StandardVariableBranching(self.model,self.variable,self.kStrategies,self.maxTimePerVariable,self.changing)

    def getTerminater(self) -> Terminate_base:
        
        return ImprovementBoundTerminater(self.improvementPercentage,self.instantThreshhold,self.trackData)##InstantTerminater(self.trackData)#

    def findBound(self,N,u,l,e):
        c_u = sum([i for i in range(u)])
        c_l = sum([i for i in range(l)])
        max_objective = None

        max_g_u = N // u  # Start with maximum feasible g_u

        for g_u in range(max_g_u, -1, -1):  # Iterate from max_g_u down to 0
            if (N - g_u * u) % l == 0:
                g_l = (N - g_u * u) // l
                if g_l >= 0:
                    objective_value = c_u * g_u + c_l * g_l
                    if max_objective is None or objective_value > max_objective:
                        max_objective = objective_value

        return max_objective*e
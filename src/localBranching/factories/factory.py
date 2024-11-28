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
        self.variable = ['meetsAtEInG','meetsAtE','meets']
        self.kStrategies = [PercentageK(0.10),FixedK(200),FixedK(200)]#0.01 for meetsAtEInG#[0.15,0.15,0.15]
        self.trackData = trackData
        self.maxTimePerVariable = 30 # only does something if multiple variables are used
        self.changing = False
        self.improvementPercentage = 0.02
        self.instantThreshhold = 15

    def getBrancher(self) -> Brancher_base:
        
        return StandardVariableBranching(self.model,self.variable,self.kStrategies,self.maxTimePerVariable,self.changing)

    def getTerminater(self) -> Terminate_base:
        
        return ImprovementBoundTerminater(self.improvementPercentage,self.instantThreshhold,self.trackData)#
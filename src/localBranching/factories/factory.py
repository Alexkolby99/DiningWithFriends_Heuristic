from typing import Dict
from src.localBranching._interfaces import Brancher_base, Terminate_base
from src.localBranching.branchingStrategies import StandardVariableBranching
from src.localBranching.branchingStrategies.kStrategies import PercentageK
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
        self.variable = ['meetsAtEInG']#['meetsAtEInG','meetsAtE','meets']
        self.percentage = [0.01]#0.01 for meetsAtEInG#[0.15,0.15,0.15]
        self.trackData = trackData
        self.maxTimePerVariable = 30
        self.changing = False
        self.improvementPercentage = 0.02
        self.instantThreshhold = 15

    def getBrancher(self) -> Brancher_base:
        
        kStrategies = [PercentageK(percentage) for percentage in self.percentage]

        return StandardVariableBranching(self.model,self.variable,kStrategies,self.maxTimePerVariable,self.changing)

    def getTerminater(self) -> Terminate_base:
        
        return InstantTerminater(self.trackData)#ImprovementBoundTerminater(self.improvementPercentage,self.instantThreshhold,self.trackData)#
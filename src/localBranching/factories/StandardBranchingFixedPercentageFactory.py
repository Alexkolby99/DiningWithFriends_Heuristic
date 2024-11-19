from typing import Dict
from src.localBranching._interfaces import Brancher_base, Terminate_base
from src.localBranching.branchingStrategies import StandardVariableBranching
from src.localBranching.branchingStrategies.kStrategies import PercentageK
from src.localBranching.terminateStrategies import InstantTerminater
from gurobipyModel import DinnerWithFriendsSolver


class StandardBranchingFixedPercentageFactory:

    def __init__(self,data: Dict,trackData: bool) -> None:
        self.model = DinnerWithFriendsSolver()
        self.model.readData(data)
        self.model.setFeasibleSolution()
        self.variable = ['meets','meetsAtE','meetsAtEInG']
        self.percentage = [0.15,0.10,0.05]
        self.trackData = trackData

    def getBrancher(self) -> Brancher_base:
        
        kStrategies = [PercentageK(percentage) for percentage in self.percentage]

        return StandardVariableBranching(self.model,self.variable,kStrategies)

    def getTerminater(self) -> Terminate_base:
        
        return InstantTerminater(self.trackData)
from typing import Dict
from src.localBranching._interfaces import Brancher_base, Terminate_base
from src.localBranching.branchingStrategies import SingleVariableBranching
from src.localBranching.branchingStrategies.kStrategies import PercentageK
from src.localBranching.terminateStrategies import InstantTerminater
from gurobipyModel import DinnerWithFriendsSolver


class SingleBranchingFixedPercentageFactory:

    def __init__(self,data: Dict,percentage: float,trackData: bool) -> None:
        self.model = DinnerWithFriendsSolver()
        self.model.readData(data)
        self.model.setFeasibleSolution()
        self.variable = self.model.meets
        self.percentage = percentage
        self.trackData = trackData

    def getBrancher(self) -> Brancher_base:
        
        return SingleVariableBranching(self.model,self.variable,PercentageK(self.percentage))

    def getTerminater(self) -> Terminate_base:
        
        return InstantTerminater(self.trackData)
from typing import Dict, List, Literal
from src.localBranching._interfaces import Brancher_base, Terminate_base
from src.localBranching.branchingStrategies import StandardVariableBranching
from src.localBranching.terminateStrategies import InstantTerminater, ImprovementBoundTerminater
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.model.factories import MaximizeMeetsFactory
from src.localBranching.branchingStrategies._interfaces import KStrategy_base


class Factory:

    def __init__(self,
                 data: Dict,
                 trackData: bool,
                 variables: List[Literal['meets','meetsAtE','meetsAtEInG']],
                 kStrategies: List[KStrategy_base],
                 maxTimePerVariable: int,
                 ImprovementPercentage: float,
                 InstantTerminationThreshhold: int,
                 strategy: List[Literal['changing','cycling','restarting']]) -> None:
        
        for v in variables:
            assert v in ['meets','meetsAtE','meetsAtEInG'], "Variable not allowed"

        assert len(variables) == len(kStrategies), "Different number of kstrategies and variables are given"

        assert strategy in ['changing','cycling','restarting'], 'The given strategy is not allowed'

        self.model = DinnerWithFriendsSolver(MaximizeMeetsFactory())
        self.model.readData(data)
        self.model.model.setParam("DegenMoves", 1) # avoid these moves since takes a while without much benefits when not solving for optimality
        #self.model.model.setParam('MIPFocus', 1) # focus on finding good feasible solutions rather than optimality
        self.model.setFeasibleSolution()
        self.variable = variables
        self.kStrategies = kStrategies
        self.trackData = trackData
        self.maxTimePerVariable = maxTimePerVariable # only does something if multiple variables are used
        self.improvementPercentage = ImprovementPercentage
        self.instantThreshhold = InstantTerminationThreshhold

        # Only one can be True of these set by the strategy given if both are false the cycling approach is used

        self.changing = False
        self.restarting = False
        if strategy != 'cycling':
            setattr(self,strategy,True)

    def getBrancher(self) -> Brancher_base:
        
        return StandardVariableBranching(self.model,
                                         self.variable,
                                         self.kStrategies,
                                         self.instantThreshhold,
                                        self.maxTimePerVariable,
                                        self.changing,
                                        self.restarting)

    def getTerminater(self) -> Terminate_base:
        
        return ImprovementBoundTerminater(self.improvementPercentage,
                                          self.instantThreshhold,
                                          self.trackData)


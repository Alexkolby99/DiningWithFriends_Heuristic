from typing import Dict, List, Literal
from src.localBranching import LocalBranching
from src.localBranching.factories import SingleBranchingFixedPercentageFactory

if __name__ == '__main__':

    l = 4
    u = 5
    n_events = 6
    n_girls = 8
    n_boys = 8

    data: Dict = {   "n_girls": n_girls,
            "n_boys": n_boys,
            "numOfEvents": n_events,
            "minNumGuests": l,
            "maxNumGuests": u
            }
    percentage: float = 0.15
    trackData: bool = True
    trackingPath: str = None
    timeLimit = 3600

    factory = SingleBranchingFixedPercentageFactory(data,percentage,trackData)
    LB_Algo = LocalBranching(factory,trackingPath)
    LB_Algo.performLocalBranching(timeLimit)
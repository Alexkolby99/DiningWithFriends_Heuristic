import os
from typing import Dict
from src.localBranching import LocalBranching
from src.localBranching.factories import StandardBranchingFixedPercentageFactory

resultFolder = os.path.join('results','properResults','15PercentageK_Combined')
timeLimit = 30             
trackData: bool = True

if __name__ == '__main__':
        l = 4
        u = 5
        n_events = 6
        for i in [21,22,23,24,25,26,27,28]:

                n_girls = i // 2
                n_boys = i-n_girls

                data: Dict = {   "n_girls": n_girls,
                        "n_boys": n_boys,
                        "numOfEvents": n_events,
                        "minNumGuests": l,
                        "maxNumGuests": u
                        }

                trackingFileName: str  = f'Tracking_size{i}.csv'
                solutionFileName: str = f'HeuristicSolution_size{i}.json'
                trackingPath: str = os.path.join(resultFolder,trackingFileName)
                solutionPath: str = os.path.join(resultFolder,solutionFileName)

                factory = StandardBranchingFixedPercentageFactory(data,trackData)
                LB_Algo = LocalBranching(factory,trackingPath)
                bestObj, Solution = LB_Algo.performLocalBranching(timeLimit)
                with open(solutionPath, "w") as outfile:
                        outfile.write(Solution)
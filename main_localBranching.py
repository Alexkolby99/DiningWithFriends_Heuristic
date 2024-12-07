import os
from typing import Dict
from src.localBranching import LocalBranching
from src.localBranching.factories import Factory


resultFolder = os.path.join('results','3events','Cycling')
timeLimit = 1800     
trackData: bool = True

'''
17: initialize with 7,10 (l,u)=(3,4)
18: initialize with 9,9 (l,u)=(3,4)
19: initialize with 8,11 (l,u)=(3,4)
'''

nGirls_getter = lambda x: x // 2 if not x in (17,19) else 7 if x == 17 else 8 
groupSize_getter = lambda x: (4,5) if not x in (17,18,19,20) else (4,4) if x == 20 else (3,4) 

if __name__ == '__main__':
        n_events = 3
        for i in [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]:

                l,u = groupSize_getter(i)
                n_girls = nGirls_getter(i)
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

                factory = Factory(data,trackData)
                LB_Algo = LocalBranching(factory,trackingPath)
                bestObj, Solution = LB_Algo.performLocalBranching(timeLimit)
                with open(solutionPath, "w") as outfile:
                        outfile.write(Solution)
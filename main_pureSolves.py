import os
import time
from typing import Dict

import numpy as np
import pandas as pd
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.model.factories import MaximizeMeetsFactory

resultFolder = os.path.join('results','3events','PureSolveSolutions')
timeLimit =  1800

nGirls_getter = lambda x: x // 2 if not x in (17,19) else 7 if x == 17 else 8 
groupSize_getter = lambda x: (4,5) if not x in (17,18,19,20) else (4,4) if x == 20 else (3,4) 


if __name__ == '__main__':
        n_events = 7
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
                trackingPath: str = os.path.join(resultFolder,trackingFileName)
                solver = DinnerWithFriendsSolver(MaximizeMeetsFactory())
                solver.readData(data)
                solver.setFeasibleSolution()
                # start = time.time()
                # objValues, runTime = solver.solveModel(timeLimit)
                # end = time.time()
                # runTime.append(end)
                # objValues.append(objValues[-1])
                # df = pd.DataFrame({'runTime':np.array(runTime) - np.array(start),
                #                    'Value':objValues,})
                # df['BestBound'] = solver.model.ObjBound
                # df.to_csv(trackingPath)
                pass

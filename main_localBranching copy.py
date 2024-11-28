import os
import time
from typing import Dict

import numpy as np
import pandas as pd
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.model.factories import MaximizeMeetsFactory

resultFolder = os.path.join('results','properResults','PureSolveSolutions')
timeLimit =  3600

if __name__ == '__main__':
        l = 4
        u = 5
        n_events = 6
        for i in [22,23,24,25,26,27,28]:

                n_girls = 12#i // 2
                n_boys = 6#-n_girls

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
                start = time.time()
                objValues, runTime = solver.solveModel(timeLimit)
                df = pd.DataFrame({'runTime':np.array(runTime) - np.array(start),
                                   'Value':objValues,})
                df.to_csv(trackingPath)
                pass

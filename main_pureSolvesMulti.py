import json
import os
import time
from typing import Dict

import numpy as np
import pandas as pd
from src.model.factories.maximizeFewestMeetsFactory import MaximizeFewestMeetsFactory
from src.model.factories.maximizeHostsFactory import MaximizeHostsFactory
from src.model.gurobipyModel import DinnerWithFriendsSolver
from src.model.factories import MaximizeMeetsFactory

resultFolder = os.path.join('results','multiObj','PureSolveSolutions')
timeLimit =  900

nGirls_getter = lambda x: x // 2 if not x in (17,19) else 7 if x == 17 else 8 
groupSize_getter = lambda x: (4,5) if not x in (17,18,19,20) else (4,4) if x == 20 else (3,4) 


if __name__ == '__main__':
        for i in [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]:
                l,u = groupSize_getter(i)
                data = {"n_girls": nGirls_getter(i),
                        "n_boys": i-nGirls_getter(i),
                        "numOfEvents": 6,
                        "minNumGuests": l,
                        "maxNumGuests": u
                        }

                trackingFileName: str  = f'TrackingFewest_size{i}.csv'
                solutionFileName: str = f'HeuristicSolutionFewest_size{i}.json'
                trackingPath: str = os.path.join(resultFolder,trackingFileName)
                solutionPath: str = os.path.join(resultFolder,solutionFileName)

                with open(f'results/mainResults/Changing/HeuristicSolution_size{i}.json') as file:
                        obj = file.read()
                        solution = json.loads(obj)


                objValue = solution['SolutionInfo']['ObjVal']
                factory1 = MaximizeFewestMeetsFactory(objValue)
                solver = DinnerWithFriendsSolver(factory1)
                solver.readData(data)
                for var in solution['Vars']:
                        solver.model.getVarByName(var['VarName']).Start = var['X']
                solver.model.update()
                start = time.time()
                objValues, runTime = solver.solveModel(timeLimit)
                df = pd.DataFrame({'runTime':np.array(runTime) - np.array(start),
                        'Value':objValues,})
                df.to_csv(trackingPath)

                trackingFileName: str  = f'TrackingHost_size{i}.csv'
                solutionFileName: str = f'HeuristicSolutionHost_size{i}.json'
                trackingPath: str = os.path.join(resultFolder,trackingFileName)
                solutionPath: str = os.path.join(resultFolder,solutionFileName)

                factory1 = MaximizeHostsFactory(objValue,solver.model.ObjVal)
                solver2 = DinnerWithFriendsSolver(factory1)
                solver2.readData(data)
                solution = solver.model.getJSONSolution()
                solution = json.loads(solution)
                for var in solution['Vars']:
                        solver2.model.getVarByName(var['VarName']).Start = var['X']
                solver2.model.update()
                start = time.time()
                objValues, runTime = solver2.solveModel(timeLimit)
                df = pd.DataFrame({'runTime':np.array(runTime) - np.array(start),
                        'Value':objValues,})
                df.to_csv(trackingPath)
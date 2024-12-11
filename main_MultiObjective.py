import json
import os
from typing import Dict
from src.localBranching import LocalBranching
from src.localBranching.factories import Factory
from src.model.factories.maximizeFewestMeetsFactory import MaximizeFewestMeetsFactory
from src.model.factories.maximizeHostsFactory import MaximizeHostsFactory
from src.model.gurobipyModel import DinnerWithFriendsSolver


resultFolder = os.path.join('results','multiObj')
timeLimit = 900
trackData: bool = True

'''
17: initialize with 7,10 (l,u)=(3,4)
18: initialize with 9,9 (l,u)=(3,4)
19: initialize with 8,11 (l,u)=(3,4)
'''

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

                factory = Factory(data,trackData)
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
                factory.model = solver
                LB_Algo = LocalBranching(factory,trackingPath)
                bestObj, solution = LB_Algo.performLocalBranching(timeLimit)
                with open(solutionPath, "w") as outfile:
                        outfile.write(solution)
                pass

                trackingFileName: str  = f'TrackingHost_size{i}.csv'
                solutionFileName: str = f'HeuristicSolutionHost_size{i}.json'
                trackingPath: str = os.path.join(resultFolder,trackingFileName)
                solutionPath: str = os.path.join(resultFolder,solutionFileName)

                factory1 = MaximizeHostsFactory(objValue,bestObj)
                solver2 = DinnerWithFriendsSolver(factory1)
                solver2.readData(data)
                solution = json.loads(solution)
                for var in solution['Vars']:
                        solver2.model.getVarByName(var['VarName']).Start = var['X']
                solver2.model.update()
                factory = Factory(data,trackData)
                factory.model = solver2
                LB_Algo = LocalBranching(factory,trackingPath)
                bestObj, solution = LB_Algo.performLocalBranching(timeLimit)
                with open(solutionPath, "w") as outfile:
                        outfile.write(solution)
                pass
                
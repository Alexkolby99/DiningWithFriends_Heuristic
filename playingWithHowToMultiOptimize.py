import numpy as np
import pandas as pd
from src.model.factories import MaximizeFewestMeetsFactory, MaximizeMeetsFactory, MaximizeHostsFactory
from src.model import DinnerWithFriendsSolver
import json

from src.localBranching import LocalBranching
from src.localBranching.factories import Factory

nGirls_getter = lambda x: x // 2 if not x in (17,19) else 7 if x == 17 else 8 
groupSize_getter = lambda x: (4,5) if not x in (17,18,19,20) else (4,4) if x == 20 else (3,4) 

df = pd.DataFrame()

for size in range(20,30):
   
    l,u = groupSize_getter(size)
    data = {"n_girls": nGirls_getter(size),
            "n_boys": size-nGirls_getter(size),
            "numOfEvents": 6,
            "minNumGuests": l,
            "maxNumGuests": u
            }

    F = Factory(data,False)

    with open(f'results/mainResults/Changing/HeuristicSolution_size{size}.json') as file:
        obj = file.read()
        solution = json.loads(obj)


    objValue = solution['SolutionInfo']['ObjVal']
    factory1 = MaximizeFewestMeetsFactory(objValue)
    solver = DinnerWithFriendsSolver(factory1)
    solver.readData(data)
    for var in solution['Vars']:
        solver.model.getVarByName(var['VarName']).Start = var['X']
    solver.model.update()

    F.model = solver

    brancher = LocalBranching(F,None)

    brancher.performLocalBranching(900)
    pass

    #solver.model.optimize()

    


    # fewestMeets = solver.model.ObjVal
    # objValue = sum([x.X for x in solver.meets.values()])

    # df.loc[size,['Type','ObjValue']] = ['FewestMeets',fewestMeets]
    # df.loc[size,['Type','RunTime']] = ['FewestMeets',np.round(solver.model.Runtime,2)]


    # factory2 = MaximizeHostsFactory(objValue,fewestMeets)

    # solver = DinnerWithFriendsSolver(factory2)
    # solver.readData(data)
    # for var in solution['Vars']:
    #     solver.model.getVarByName(var['VarName']).Start = var['X']
    # solver.model.update()
    # solver.model.optimize()

    # df2 = pd.DataFrame({'Type': 'NumberOfDifferentHosts',
    #               'ObjValue':solver.model.ObjVal,
    #               'RunTime':np.round(solver.model.Runtime,2)},index=[size])
    # df = pd.concat([df,df2])
    # pass










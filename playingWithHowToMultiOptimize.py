from src.model.factories import MaximizeFewestMeetsFactory, MaximizeMeetsFactory, MaximizeHostsFactory
from src.model import DinnerWithFriendsSolver
import json

data = {"n_girls": 8,
        "n_boys": 8,
        "numOfEvents": 6,
        "minNumGuests": 4,
        "maxNumGuests": 5
        }

with open('results/properResults/15PercentageK_Cycling/HeuristicSolution_size16.json') as file:
    obj = file.read()
    solution = json.loads(obj)



factory = MaximizeHostsFactory(120,15)

solver = DinnerWithFriendsSolver(factory)
solver.readData(data)

for var in solution['Vars']:
    solver.model.getVarByName(var['VarName']).Start = var['X']


solver.model.update()

solver.model.optimize()

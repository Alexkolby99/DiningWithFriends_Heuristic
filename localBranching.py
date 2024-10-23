import json
import math
import numpy as np
from src.cascadeGrouping import CascadeGrouping
from gurobipyModel import DinnerWithFriendsSolver

def read_json_to_dict(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

file = 'testInstances/testInstance01.json'

data = read_json_to_dict(file)

n_girls = data['n_girls']
n_boys = data['n_boys']
N = n_girls+n_boys
E = data['numOfEvents']
l = data['minNumGuests']
u = data['maxNumGuests']
students = data['Girls'] + data['Boys']

n_groups = math.ceil(N / l)

construction = CascadeGrouping(n_girls,n_boys,l,u)
solution = construction.constructSolution(E)

# pairs = []

# for i in range(0, N - 1):
#     for j in range(i + 1, N):
#         pairs.append((students[i], students[j]))


# ### decision variables to use in the gurobi py model

# # Decision variables for pupils meeting at least once during the events
# meets = {pair: 0 for pair in pairs}
# # Decision variables for pupils meeting at a specific event
# meetsAtE = {e: {pair: 0 for pair in pairs} for e in range(E)}
# # Decision variables for pupils meeting in a group at a specific event
# meetsAtEInG = {e : {g: {pair: 0 for pair in pairs} for g in range(n_groups)} for e in range(E)}
# # Decision variables for pupils being in a group at a specific event
# isInGroupAtE = {e : {g: {kid: 0 for kid in students} for g in range(n_groups)} for e in range(E)}
# # Decision variables for whether a group is in use at an event
# groupInUse = {e: {g: 0 for g in range(n_groups)} for e in range(E)}
# # Decision variables for one pupil visiting another at an Event
# visits = {e : {kid1: {kid2: 0 for kid2 in students} for kid1 in students} for e in range(E)}
# # Decision variables for whether a pupil is hosting an event
# isHost = {e: {kid: 0 for kid in students} for e in range(E)}

# for eventNum,sol in enumerate(solution[1:]):
#     for idx,g in enumerate(sol.groups):
#         host = students[g.host.identifier]
#         if len(g.members) != 0:
#             groupInUse[eventNum][idx] = 1
        
#         isHost[eventNum][host] = 1

#         for m1 in g.members:
#             if students[m1.identifier] != host:
#                 visits[eventNum][host][students[m1.identifier]] = 1
#             isInGroupAtE[eventNum][idx][students[m1.identifier]] = 1
#             for m2 in g.members:
#                 if m1 != m2:
#                     pair = (min(m1.identifier,m2.identifier),max(m1.identifier,m2.identifier))
#                     pair = (students[pair[0]],students[pair[1]])
#                     meets[pair] = 1
#                     meetsAtE[eventNum][pair] = 1
#                     meetsAtEInG[eventNum][idx][pair] = 1



solver = DinnerWithFriendsSolver()

solver.readData('exampleData.json')
solver.initializeModel()
solver.createVariables()
solver.setVariables(solution)
solver.buildModel()
solver.solveModel()
pass
from gurobipyModel_HeuristicOptimization import DinnerWithFriendsSolver


n_girls = 9
n_boys = 10
n_events = 1
l = 3
u = 4

data = {   "n_girls": n_girls,
"n_boys": n_boys,
"numOfEvents": n_events,
"minNumGuests": l,
"maxNumGuests": u
}


dwf = DinnerWithFriendsSolver()
dwf.readData(data)

dwf.solveModel(100000)
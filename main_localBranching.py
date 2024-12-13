import os
from typing import Dict, List, Literal
from src.localBranching import LocalBranching
from src.localBranching.branchingStrategies.kStrategies import PercentageK, FixedK
from src.localBranching.factories import Factory


# Hyper parameters
timeLimit = 1800 # The total timelimit in seconds for optimizing
trackData: bool = True # if the descent should be tracked and saved to a csv file or not
variables: List[Literal['meets','meetsAtE','meetsAtEInG']] = ['meets','meetsAtE','meetsAtEInG'] # the variables used to branch upon
kstrategies = [PercentageK(0.1),PercentageK(0.05),PercentageK(0.1)] # the corresponding k strategies for the variables
maxTimePerVariable = 120 # Max time to use per variable before moving on, Initially this is set to instantTerminationThreshhold until no solution was able to found for all variables
improvementPercentage = 0.02 # The improvement percentage bound
instantTerminationThreshhold = 30 # the threshhold in seconds for when a branch terminate as soon as an improved solution is found
strategy: List[Literal['changing','cycling','restarting']] = 'changing' # The strategy used



# The actual data for the problem
n_girls = 8
n_boys = 8
n_events = 3  
l = 4
u = 4
   
if __name__ == '__main__':

        data: Dict = {"n_girls": n_girls,
        "n_boys": n_boys,
        "numOfEvents": n_events,
        "minNumGuests": l,
        "maxNumGuests": u
        }

        factory = Factory(data,
                          trackData,
                          variables,
                          kstrategies,
                          maxTimePerVariable,
                          improvementPercentage,
                          instantTerminationThreshhold,
                          strategy)
        LB_Algo = LocalBranching(factory)
        bestObj, Solution = LB_Algo.performLocalBranching(timeLimit)
        pass
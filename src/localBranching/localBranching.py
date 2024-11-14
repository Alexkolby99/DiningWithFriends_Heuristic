from datetime import datetime
import os
import time
from typing import Tuple
from src.localBranching._interfaces.factory_base import Factory_base
from gurobipy import Model
from functools import partial

class LocalBranching:


    def __init__(self,factory: Factory_base,trackingPath = None) -> None:
        self.brancher = factory.getBrancher()
        self.terminater = factory.getTerminater()
        self.bestObj = self.brancher.initObjectiveValue
        if trackingPath is None:
            self.trackingPath = os.path.join(f'tracking_{datetime.now().strftime("%Y%m%d_%H_%M_%S")}.csv')
        else:
            self.trackingPath = trackingPath

    def performLocalBranching(self,timeLimit: float) -> Tuple[float,dict]:
        start = time.time()

        branch: Model = self.brancher.nextBranch(None,self.bestObj,timeLimit)
        while True:
            branch.optimize(self.terminater.callback)
            objValue = branch.ObjVal
            timeLeft = timeLimit - (time.time() - start)
            
            if timeLeft <= 0:
                break
            
            branch = self.brancher.nextBranch(objValue,self.bestObj,timeLeft)

            if objValue > self.bestObj:
                self.bestObj = objValue

            if branch is None:
                break
            

        solution = None
        self.terminater.saveTracking(start,self.brancher.initObjectiveValue,self.trackingPath)
        return self.bestObj, solution

            
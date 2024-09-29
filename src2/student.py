import numpy as np
from src.interfaces import student_Base

class student(student_Base):

    def __init__(self,type,number,numberOfEvents,numberOfStudents):
        self._type = type
        self._number = number
        self._hostTimes = 0
        self._hostEvents = [False] * numberOfEvents
        self._groupingOptions = np.zeros((numberOfEvents,numberOfStudents),dtype=bool)
        self._groupingOptions = ~self._groupingOptions
        self._groupingOptions[:,number] = False
        self._group = [None] * numberOfEvents
        self._canVisit = [True] * numberOfStudents
        self._canVisit[self.number] = False
    

    @property
    def canVisit(self):
        return self._canVisit

    def hasVisited(self,student):

        self._canVisit[student.number] = False

    @property
    def groupingOptions(self):
        return self._groupingOptions

    def getGroupOptions(self,t):
        return self.groupingOptions[t]

    @property
    def type(self):
        return self._type
    
    @property
    def number(self):
        return self._number
    
    @property
    def hostTimes(self):
        return self._hostTimes

    @property
    def hostEvents(self):
        return self._hostEvents

    @property
    def group(self):
        return self._group
    
    @group.setter
    def group(self,group):
        self._group = group

    def setGroup(self,group,t):
        self.group[t] = group
    
    def setHostTime(self,t):
        if not self._hostEvents[t]:
            self.hostEvents[t] = True
            self._hostTimes += 1
    
    def removeHostTime(self,t):
        if self.hostEvents[t]:
            self.hostEvents[t] = False
            self.hostTimes -= 1

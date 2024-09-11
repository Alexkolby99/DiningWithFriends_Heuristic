import numpy as np
from src.interfaces import student_Base

class student(student_Base):

    def __init__(self,type,number):
        self._type = type
        self._number = number
        self._hostTimes = 0
        self._hostLastEvent = False
        # self._studentsGroupedWith = np.array([])
        # self._studentsGroupedWithLast = np.array([])
        # self._possibleStudentsToGroupWith = np.array([])
        self._group = None

    @property
    def type(self):
        return self._type
    
    @property
    def number(self):
        return self._number
    
    @property
    def hostTimes(self):
        return self._hostTimes
    
    @hostTimes.setter
    def hostTimes(self,value):
        self._hostTimes = value
   
    def addHostTime(self,value):
        self.hostTimes += value

    @property
    def hostLastEvent(self):
        return self._hostLastEvent
    
    @hostLastEvent.setter
    def hostLastevent(self,value):
        self._hostLastEvent = value

    @property
    def group(self):
        return self._group
    
    @group.setter
    def group(self,group):
        self._group = group

    def addGroupedWith(self,student):
        pass

    def addGroupedWithLast(self,student):
        pass
    
    def addHostTime(self,student):
        pass

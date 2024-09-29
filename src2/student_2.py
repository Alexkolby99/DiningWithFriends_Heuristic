import numpy as np
from src.interfaces import student_Base
from src.group_2 import group

class student():

    def __init__(self,identifier,gender,numberOfEvents):
        self._hostTimes = 0
        self._groups = [group(0,None)]*(numberOfEvents+1)
        self._studentsThatVisited = []
        self._gender = gender
        self._studentsGroupedWith = []
        self._identifier = identifier

    @property
    def hostTimes(self):
        return self._hostTimes

    def addStudentsThatVisited(self,students: list):
        self._studentsThatVisited += [s for s in students if s != self]

    def addStudentsGroupedWith(self,students: list):
        self._studentsGroupedWith += [s for s in students if s != self]

    def addHostTime(self):
        self._hostTimes += 1

    def removeHostTime(self):
        self._hostTimes -= 1
    
    @property
    def groups(self):
        return self._groups
    
    def assignGroup(self,group):
        self._groups[group.timeStamp] = group

    @property
    def studentsThatVisited(self):
        return self._studentsThatVisited
    
    @property
    def gender(self):
        return self._gender
    
    @property
    def studentsGroupedWith(self):
        return self._studentsGroupedWith
    
    @property
    def identifier(self):
        return self._identifier
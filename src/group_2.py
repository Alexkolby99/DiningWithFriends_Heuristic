import numpy as np
from src import student, group
from src.interfaces import group_Base

class group():

    def __init__(self,t,host=None) -> None:
        self._t = t
        self._host = host
        self._members = []
        self._invalidOptions = []
        self._validSize = False
        self._genderCount = [0,0]
        self._validHost = False
        self._validGender = False
        if host is not None:
            self.addMember(host)
            self._invalidOptions = set(self._invalidOptions).union(set(host.studentsThatVisited))
    
    @property
    def genderCount(self):
        return self._genderCount

    @property
    def timeStamp(self):
        return self._t

    @property
    def validSize(self):
        return self._validSize

    @property
    def validHost(self):
        return self._validHost
    
    @property 
    def validGender(self):
        return self._validGender

    @property
    def size(self):
        return len(self._members)

    @property
    def invalidOptions(self):
        return self._invalidOptions

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self,host):
        
        self._invalidOptions = set()
        for member in self._members:
            self._invalidOptions = set(member.groups[self.timeStamp-1].members).union(set(self._invalidOptions))

        self._invalidOptions = set(host.studentsThatVisited).union(set(self._invalidOptions))
        self._host = host

    @property
    def members(self):
        return self._members
    
    def addMember(self,member: student):
        
        self._members = self._members + [member]
        member.assignGroup(self)
        self._invalidOptions = set(member.groups[self.timeStamp-1].members).union(set(self._invalidOptions))
        self._genderCount[member.gender] += 1

    def removeMember(self,member: student):
        self._members.remove(member)
        self._invalidOptions = set([m for member in self._members for m in member.groups[self.timeStamp-1].members])
        self._genderCount[member.gender] -= 1

    def __str__(self):

        return f'''
                host is student {self.host.identifier} with gender {self.host.gender}\n
                group has gender count: {self.genderCount}\n
                members are: {[member.identifier for member in self.members]}\n
                invalidOptions are: {[option.identifier for option in self.invalidOptions]}
                '''
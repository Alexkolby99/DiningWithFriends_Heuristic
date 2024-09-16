import numpy as np
from src import student, group
from src.interfaces import group_Base

class group(group_Base):

    def __init__(self,N,t,preGroups,size_min,size_max) -> None:
        self._host = None
        self._members = []
        self._size = 0
        self._addOptions = np.zeros(N,dtype=bool)
        self._addOptions = ~self._addOptions
        self._size_min = size_min
        self._size_max = size_max
        self.t = t
        self._preGroups = preGroups
        self._validSize = False
        self._hasHost = False

    @property
    def validSize(self):
        return self._size >= self.size_min and self._size <= self.size_max

    @property
    def hasHost(self):
        return self._hasHost

    @property
    def size_min(self):
        return self._size_min
    
    @property
    def size_max(self):
        return self._size_max

    @property
    def preGroups(self):
        return self._preGroups
    
    @property
    def size(self):
        return self._size

    @property
    def addOptions(self):
        return self._addOptions

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self,host):
        self._host = host

    @property
    def members(self):
        return self._members
    
    @members.setter
    def members(self,members):
        self._members = members

    def addMember(self,member: student):
        
        assert self.addOptions[member.number], 'Can not be assigned to this group'

        if self.size == 1:
            self._addOptions = self.members[0].getGroupOptions(self.t)

        self.members = self.members + [member]
        self._addOptions = np.logical_and(self.addOptions, member.getGroupOptions(self.t))
        self._size += 1

        if self.size == 1:
            self._addOptions[np.array(self.preGroups) != member.type] = False


    def removeMember(self,member):
        self.members.remove(member)

    def canMerge(self,group: group):

        if self.size + group.size > self.size_max:
            return False

        groupFitInSelf = all(self.addOptions[[member.number for member in group.members]])
        selfFitInGroup = all(group.addOptions[[member.number for member in self.members]])

        return groupFitInSelf and selfFitInGroup
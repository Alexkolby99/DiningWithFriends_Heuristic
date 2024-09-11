import numpy as np
from src.interfaces import group_Base

class group(group_Base):

    def __init__(self) -> None:
        self._host = None
        self._members = []

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

    def addMember(self,student):
        
        self.members = self.members + [student]

    def removeMember(self,member):
        self.members.remove(member)
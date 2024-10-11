
from typing import List, Literal
from src.interfaces import group_Base

class Group(group_Base):
    def __init__(self, host: 'student', timestamp: int) -> None:
        self._members: List['student'] = []
        self._host = host
        self._timestamp = timestamp
        self._genderCount = [0,0]

        if host is not None:
            self.addMember(host)

    @property
    def members(self) -> List['student']:
        return self._members

    @property
    def host(self) -> 'student':
        return self._host

    @host.setter
    def host(self,student):
        self._host = student

    @property
    def size(self) -> int:
        return len(self._members)

    @property
    def t(self) -> int:
        return self._timestamp
    
    @t.setter
    def t(self,t):
        self._timestamp = t

    def addMember(self, member: 'student') -> None:
        '''Add a member to the group'''
        if member not in self._members:
            self._members.append(member)
            self._genderCount[member.gender] += 1
        else:
            print(f"{member} is already a member of the group.")

    def removeMember(self, member: 'student') -> None:
        '''Remove a member from the group'''
        if member in self._members:
            self._members.remove(member)
            self._genderCount[member.gender] -= 1
            if member == self._host:
                self._host == None
        else:
            print(f"{member} is not a member of the group.")

    def getGenderCount(self,gender: Literal[0,1]):

        return self._genderCount[gender]
    
    def  __str__(self):

        return f'''
                host is student {self.host.identifier if self.host is not None else None} with gender {self.host.gender if self.host is not None else None}\n
                group has gender count: {self._genderCount}\n
                members are: {[member.identifier for member in self.members]}\n
                '''
    #invalidOptions are: {set([m.identifier for member in self.members for m in member.groups[self.t-1].members] + [m.identifier for m in self.host.studentsThatVisited if self.host is not None])}
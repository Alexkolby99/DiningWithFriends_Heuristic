from src.interfaces import event_Base
from src import group

class event():

    def __init__(self,t) -> None:
        self._timeStamp = t
        self._groups = []
        self._hosts = []

    @property
    def timestamp(self):
        return self._timeStamp

    @property
    def groups(self):
        return self._groups
    
    @property
    def hosts(self):
        return self._hosts
    
    def addGroups(self,groups: list[group] | group): 
        if not isinstance(groups,list):   
            groups = [groups] 
        self._groups = self._groups + groups
        self._hosts = self._hosts + [g.host for g in groups]

        for group in groups:
            for member in group.members:
                if group.host == member:
                    member.addHostTime()
                    member.addStudentsThatVisited(group.members)
                
                member.addStudentsGroupedWith(group.members)


    def __str__(self):

        out_str = f'Event at timestamp {self.timestamp} has NumberOfGroups = {len(self.groups)}\n'

        for i,g in enumerate(self.groups):
            out_str += f'Group {i} is:\n' 
            out_str += g.__str__()
            out_str += '\n'

        return out_str
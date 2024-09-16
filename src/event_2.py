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

from src.interfaces import event_Base

class event(event_Base):

    def __init__(self,t) -> None:
        self._timeStamp = t
        self._groups = []
        self.invalidGroups = []

    @property
    def timestamp(self):
        return self._timeStamp

    @timestamp.setter
    def timestamp(self,timestamp):
        self._timeStamp = timestamp

    @property
    def groups(self):
        return self._groups
    
    @groups.setter
    def groups(self,groups):
        self._groups = groups

    def addGroup(self,group):
        
        self.groups = self.groups + [group]

    def removeGroup(self,group):
        
        self.groups.remove(group)
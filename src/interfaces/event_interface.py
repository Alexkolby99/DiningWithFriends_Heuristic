from abc import abstractmethod, ABC

class event_Base(ABC):

    @property
    @abstractmethod
    def timestamp(self):
        pass

    @property
    @abstractmethod
    def groups(self):
        pass

    @abstractmethod
    def addGroup(self,group):
        pass

    @abstractmethod
    def removeGroup(self,group):
        pass
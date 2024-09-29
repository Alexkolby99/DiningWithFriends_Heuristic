from abc import abstractmethod, ABC

class group_Base(ABC):

    @property
    @abstractmethod
    def members(self):
        pass

    @property
    @abstractmethod
    def host(self):
        pass

    @abstractmethod
    def addMember(self,member):
        pass

    @abstractmethod
    def removeMember(self,member):
        pass
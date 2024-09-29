from abc import ABC, abstractmethod

class student_Base(ABC):

    @property
    @abstractmethod
    def type(self):
        pass
    
    @property
    @abstractmethod
    def number(self):
        pass

    @property
    @abstractmethod
    def hostTimes(self):
        pass

    @property
    @abstractmethod
    def hostEvents(self):
        pass

    @property
    @abstractmethod
    def group(self):
        pass

    @abstractmethod
    def setHostTime(self,t):
        pass

    @abstractmethod
    def removeHostTime(self,t):
        pass

    @abstractmethod 
    def setGroup(self,group,t):
        pass
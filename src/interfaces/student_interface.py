from abc import ABC, abstractmethod

class student_Base(ABC):

    @abstractmethod
    def addGroupedWith(self):
        pass

    @abstractmethod
    def addGroupedWithLast(self):
        pass

    @abstractmethod
    def addHostTime(self):
        pass
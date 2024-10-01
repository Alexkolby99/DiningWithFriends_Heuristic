from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class InsertMove(ConstructionMove_base):

    def __init__(self,max_size) -> None:
        self.max_size = max_size

    def performMove(self, student: Student, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for group in groups:
            if self.__canAdd(student,group):
                group.addMember(student)
                return True

        return False

    
    def __canAdd(self,student: Student,group: Group):

        if group.size == self.max_size:
            return False

        if student in group.host.studentsThatVisited:
            return False

        if group.getGenderCount(student.gender) == 0:
            return False

        for member in group.members:
            if student in member.groups[group.t-1].members:
                return False

        return True
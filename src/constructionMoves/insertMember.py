from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class InsertMember(ConstructionMove_base):

    def performMove(self, student: Student, groups: List[Group],t: int) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for group in groups:
            if self.__canAdd(student,group,t):
                group.addMember(student)
                return True

        return False

    
    def __canAdd(self,student: Student,group: Group,t: int):

        for member in group.members:
            if student in member.groups[t-1].members:
                continue
            if group.getGenderCount(student.gender) == 0:
                continue
            if student in group.host.studentsThatVisited:
                continue
            return True

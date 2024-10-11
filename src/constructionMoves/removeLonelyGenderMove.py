from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class RemoveLonelyGenderMove(ConstructionMove_base):

    def __init__(self,min_size, max_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        if self.min_size == group.size:
            return False

        if group.getGenderCount(0) != 1 and group.getGenderCount(1) != 1:
            return True
        
        lonelyGender = 0 if group.getGenderCount(0) == 1 else 1
    
        for student in group.members:
            if student.gender == lonelyGender:
                for g2 in groups:
                    if g2 != group:
                        if self.__canAdd(student,g2):
                            group.removeMember(student)
                            g2.addMember(student)
                            return True

        return False

    
    def __canAdd(self,student: Student,group: Group):

        if group.size == self.max_size:
            return False

        if group.host is not None:
            if student in group.host.studentsThatVisited:
                return False

        if group.getGenderCount(student.gender) == 0:
            return False

        for member in group.members:
            if student in member.groups[group.t-1].members:
                return False

        return True
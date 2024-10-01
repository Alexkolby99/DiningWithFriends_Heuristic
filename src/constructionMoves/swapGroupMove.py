from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class SwapGroupMove(ConstructionMove_base):

    def __init__(self,max_size,min_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for g1 in groups:
            for m in self.__canRemove(g1):
                if self.__canAdd(m,group):
                    g1.removeMember(m)
                    group.addMember(m)
                    return True
        
        return False

    
    def __canRemove(self,group: Group) -> List[Student]:
        

        if group.size == self.min_size:
            return []

        canRemoveOneFromGender = [group.getGenderCount(0) > 2,group.getGenderCount(1) > 2]

        members_CanRemove = []

        for m in group.members:
            if group.host == m:
                continue
            if canRemoveOneFromGender[m.gender]:
                members_CanRemove.append(m)           

        return members_CanRemove 
        

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
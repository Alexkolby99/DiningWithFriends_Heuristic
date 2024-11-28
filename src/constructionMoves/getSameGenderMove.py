from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class GetSameGenderMove(ConstructionMove_base):

    def __init__(self,min_size, max_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        

        if group.getGenderCount(0) != 1 and group.getGenderCount(1) != 1:
            return True
        

        lonelyGender = 0 if group.getGenderCount(0) == 1 else 1

        if group.size == self.min_size: # can potentially just add the person to the group
            for g2 in groups:
                if g2 != group:
                    for m2 in g2.members[:]:
                        if m2.gender == lonelyGender and g2.getGenderCount(lonelyGender) != 2:
                            g2.removeMember(m2)
                            if g2.size < self.min_size: #== self.min_size:
                                # might need to handle that someone else can be swapped to here
                                for m1 in group.members[:]:
                                    if m1.gender != lonelyGender:
                                        group.removeMember(m1)
                                        if self.__canAdd(m2,group) and self.__canAdd(m1,g2):
                                            g2.addMember(m1)
                                            group.addMember(m2)
                                            return True
                                    
                                    group.addMember(m1)
                            else:
                                if self.__canRemove(m2,g2):
                                    if self.__canAdd(m2,group):
                                        g2.removeMember(m2)
                                        group.addMember(m2)
                                        return True
                                
                                for m1 in group.members[:]:
                                    if m1.gender != lonelyGender:
                                        group.removeMember(m1)
                                        if self.__canAdd(m2,group) and self.__canAdd(m1,g2):
                                            g2.addMember(m1)
                                            group.addMember(m2)
                                            return True
                                    
                                    group.addMember(m1)
                            g2.addMember(m2)
        
        else: # need to swap
            for m in group.members[:]:
                if m.gender != lonelyGender:
                    group.removeMember(m)
                    for g2 in groups:
                        if g2 != group:
                            for m2 in g2.members[:]:
                                if m2.gender == lonelyGender:
                                    g2.removeMember(m2)
                                    if self.__canAdd(m2,group) and self.__canAdd(m,g2):
                                        group.addMember(m2)
                                        g2.addMember(m)
                                        return True
                                    g2.addMember(m2)
                    
                    group.addMember(m)

            return False
    
    def __canRemove(self,student: Student, group: Group):

        if group.size == self.min_size:
            return False

        if group.getGenderCount(student.gender) == 2:
            return False
        
        return True


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
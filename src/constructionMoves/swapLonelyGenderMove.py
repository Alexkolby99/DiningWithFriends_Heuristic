from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class SwapLonelyGenderMove(ConstructionMove_base):

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

        if group.size == self.min_size: # must swap to the same group as removing from if group size is the minimum size
            for student in group.members[:]:
                if student.gender == lonelyGender:
                    group.removeMember(student)
                    for g2 in groups:
                        if g2 != group:
                            for m2 in g2.members[:]:
                                if m2.gender != lonelyGender:
                                    g2.removeMember(m2)
                                    if self.__canAdd(student,g2) and self.__canAdd(m2,group):
                                        g2.addMember(student)
                                        group.addMember(m2)
                                        return True
                                    else:
                                        g2.addMember(m2)
                
            group.addMember(student)
                             
        else: # can swap m2 to an arbitrary group if size of g2 > min_size
            for student in group.members[:]:
                if student.gender == lonelyGender:
                    group.removeMember(student)
                    for g2 in groups:
                        if g2 != group:
                            if g2.size == self.min_size:
                                for m2 in g2.members[:]:
                                    if m2.gender != lonelyGender:
                                        if g2.getGenderCount(1-lonelyGender) != 2:      
                                            g2.removeMember(m2)                            
                                            if self.__canAdd(m2,group) and self.__canAdd(student,g2):
                                                group.addMember(m2)
                                                g2.addMember(student)
                                                return True
                                        else:
                                            g2.removeMember(m2)
                                            for g3 in groups:
                                                if g3 != g2 and g3 != group:
                                                    for m3 in g3.members[:]:
                                                        if m3.gender != lonelyGender and self.__canRemove(m3,g3):  
                                                            if self.__canAdd(m3,g2):
                                                                g3.removeMember(m3)
                                                                g2.addMember(m3)
                                                                if self.__canAdd(m2,group) and self.__canAdd(student,g2):
                                                                    group.addMember(m2)
                                                                    g2.addMember(student)
                                                                    return True
                                                                g2.removeMember(m3)
                                                                g3.addMember(m3)
                                        g2.addMember(m2)
                            else: 
                                for m2 in g2.members[:]:
                                    if m2.gender != lonelyGender:
                                        if self.__canRemove(m2,g2):
                                            g2.removeMember(m2)
                                            if self.__canAdd(student,g2):
                                                g2.addMember(student)
                                                for g3 in groups:
                                                    if self.__canAdd(m2,g3):
                                                        g3.addMember(m2)
                                                        return True
                                                g2.removeMember(student)
                                            g2.addMember(m2)
            
            group.addMember(student)

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
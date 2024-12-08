from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class FindHostWithSwapsMove(ConstructionMove_base):

    def __init__(self,min_size,max_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        for m in group.members[::-1]:
            if group.host is None:
                if m.groups[group.t-1].host != m:
                    group.host = m
                    for m2 in [m2 for m2 in group.members if m2 in m.studentsThatVisited and m2 != m]:
                        status = self.checkSwap(group, groups, m, m2)
                        if status == False:
                            group.addMember(m2)
                            group.host = None  

        return True 

    def checkSwap(self, group, groups, m, m2):
        for g2 in groups:
            if g2 != group:
                for m3 in g2.members[:]:
                    if m3 != g2.host:
                        if self.__canSwap(m2,m3,g2,group):
                            g2.removeMember(m3)
                            g2.addMember(m2)
                            group.removeMember(m2)
                            group.addMember(m3)
                            return True
                    


        return False
    
    def __canSwap(self,student1: Student, student2: Student,group1: Group,group2: Group):

        if student1.gender != student2.gender:
            if group1.getGenderCount(student2.gender) == 2 or group2.getGenderCount(student1.gender)==0:
                return False
            if group2.getGenderCount(student1.gender) == 2 or group1.getGenderCount(student2.gender)==0:
                return False

        if group1.host is not None:
            if student1 in group1.host.studentsThatVisited:
                return False
            
        if group2.host is not None:
            if student2 in group2.host.studentsThatVisited:
                return False

        for member in group1.members:
            if member != student2:
                if member in student1.groups[group1.t-1].members:
                    return False

        for member in group2.members:
            if member != student1:
                if member in student2.groups[group2.t-1].members:
                    return False

        return True

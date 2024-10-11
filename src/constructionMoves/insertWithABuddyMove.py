from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class InsertWithABuddyMove(ConstructionMove_base):

    def __init__(self,min_size,max_size) -> None:
        self.max_size = max_size
        self.min_size = min_size
    def performMove(self, student: Student, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for g1 in groups:
            for m in self.__canBeGroupedWith(student,g1):
                if m == g1.host:
                    newHost = self.__findNewHost(g1)
                    if newHost is None:
                        continue
                for g2 in groups:
                    if g1 != g2:
                        if self.__canAdd(student,m,g2):
                            if m == g1.host:
                                g1.host = newHost
                            g2.addMember(student)
                            g1.removeMember(m)
                            g2.addMember(m)
                            return True

        return False

    def __canBeGroupedWith(self,student: Student ,group: Group):
        
        if group.size == self.min_size:
            return []

        canBeGroupedWith = [m for m in group.members]
        for m in group.members:
            if student in m.groups[group.t-1].members or student.gender != m.gender:
                canBeGroupedWith.remove(m)


        return canBeGroupedWith

    def __findNewHost(self,group: Group):
        host = None
        for m in group.members:
            if host is not None:
                return host
            if m == group.host: # if the current host continue
                continue
            if m.groups[group.t-1].host == m: # if m was host at last event continue
                continue
            host = m
            for m2 in group.members:
                if m2 != m:
                    if m2 not in m.studentsThatVisited or m2 == group.host: # if the member has not visited the new host yet continue
                        continue
                    else: # if one of the members has visited the new host m2 cannot be host
                        host = None
                        break
            
        return None

    def __canAdd(self,student1: Student,student2: Student,group: Group):

        if group.size >= self.max_size-1:
            return False

        for student in [student1,student2]:
            if student in group.host.studentsThatVisited:
                return False

            for member in group.members:
                if student in member.groups[group.t-1].members:
                    return False

        return True
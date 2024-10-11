from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class InsertSwapMove(ConstructionMove_base):

    def __init__(self,max_size) -> None:
        self.max_size = max_size

    def performMove(self, student: Student, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for g1 in groups:
            for m1 in self.__canSwap(student,g1):
                if g1.host == m1:
                    newHost = self.__findNewHost(m1,g1)
                    if newHost is None:
                        continue
                for g2 in groups:
                    if self.__canAdd(m1,g2):
                        if g1.host == m1:
                            g1.host = newHost
                        g1.removeMember(m1)
                        g2.addMember(m1)
                        g1.addMember(student)
                        return True
        
        return False

    def __findNewHost(self,student: Student ,group: Group):

        for m in group.members:
            if m == group.host:
                continue
            if student not in m.studentsThatVisited and m.groups[group.t-1].host != m:
                return m
        
        return None
    
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


    def __canSwap(self,memberToAdd, group: Group):

        membersThatCanSwapWith = [member for member in group.members if group.host != member] # initial all members can be swapped with
        membersThatCanSwapWith = membersThatCanSwapWith + [group.host]
        if group.getGenderCount(memberToAdd.gender) == 0:
            return []


        # outer loop is the member considered swapping with however you cannot swap with the host
        for member1 in membersThatCanSwapWith[:]:
            if group.getGenderCount(memberToAdd.gender) == 2 and member1.gender != memberToAdd.gender:
                membersThatCanSwapWith.remove(member1)
                continue
            if group.getGenderCount(member1.gender) == 2 and member1.gender != memberToAdd.gender:
                membersThatCanSwapWith.remove(member1)
                continue
            for member2 in group.members: # if the member to add does not conflict with any of the remaining in the group, it must only conflict with member1
                if member2 != member1:
                    if memberToAdd in member2.groups[group.t-1].members:
                        membersThatCanSwapWith.remove(member1)
                        break


            
        return membersThatCanSwapWith
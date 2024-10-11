from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class InsertDoubleSwapMove(ConstructionMove_base):

    def __init__(self,max_size) -> None:
        self.max_size = max_size

    def performMove(self, student: Student, groups: List[Group]) -> bool:
        """
        Performs a move with the given students and groups.
        
        Returns True if the move was successful, False otherwise.
        """
        
        for g1 in groups:
            for m1 in self.__canSwap(student,g1):
                g1.removeMember(m1)
                g1.addMember(student)
                for g2 in groups:
                    if g2 != g1:
                        for m2 in self.__canSwap(m1,g2):
                            g2.removeMember(m2)
                            g2.addMember(m1)
                            for g3 in groups:
                                if self.__canAdd(m2,g3):
                                    g3.addMember(m2)
                                    return True

                            # clean up if moving on to the next m2
                            g2.removeMember(m1)
                            g2.addMember(m2)
                # clean up if moving on to the next m1
                g1.removeMember(student)
                g1.addMember(m1)
        
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


    def __canSwap(self,memberToAdd, group: Group):

        membersThatCanSwapWith = [member for member in group.members if group.host != member] # initial all members can be swapped with

        if group.getGenderCount(memberToAdd.gender) == 0 or memberToAdd in group.host.studentsThatVisited:
            return []

        # check gender 
        # check if 

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
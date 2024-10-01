from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class Swap2ToGroupMove(ConstructionMove_base):

    def __init__(self,max_size,min_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """

        """

        if group.size - self.min_size < 2:
            return False

        for g1 in groups:
            for g2 in groups:
                for m1, m2 in self.__canRemove(g1,g2):
                    if self.__canAdd(m1,m2,group):
                        g1.removeMember(m1)
                        g2.removeMember(m2)
                        group.addMember(m1)
                        group.addMember(m2)

        
        return True
    
    def __canRemove(self,group1: Group,group2: Group):
        
        pairs_canRemove = []

        if group1 != group2:

            if group1.size == self.min_size == self.min_size or group2.size == self.min_size:
                return []

            canRemoveGender = {group1: [group1.getGenderCount(0) > 2, group2.getGenderCount(1) > 2], 
                               group2: [group1.getGenderCount(0) > 2, group2.getGenderCount(1) > 2]}
            
            for m1 in group1.members:
                if group1.host == m1:
                    continue
                for m2 in group2.members:
                    if group2.host == m2:
                        continue
                    if canRemoveGender.get(group1)[m1.gender] and canRemoveGender.get(group2)[m2.gender]:
                        if self.__canBeGrouped(m1,m2,group1.t):
                            pairs_canRemove.append((m1,m2))

            return pairs_canRemove

                    

        
        if group1 == group2:

            if group1.size <= self.min_size+1:
                return []

            canRemoveGenderCombination = {(0,1): group1.getGenderCount(0) > 2 and group1.getGenderCount(1) > 2,
                                          (0,0): group1.getGenderCount(0) > 3,
                                          (1,0): group1.getGenderCount(0) > 2 and group1.getGenderCount(1) > 2,
                                          (1,1): group1.getGenderCount(1) > 3}

            for m1 in group1.members:
                if group1.host == m1:
                    continue
                for m2 in group1.members:
                    if group1.host == m2:
                        continue
                    if m1 == m2:
                        continue

                    if canRemoveGenderCombination.get((m1.gender,m2.gender)):
                        pairs_canRemove.append((m1,m2))

        return pairs_canRemove

    def __canBeGrouped(self,m1,m2,t):
        
        if m1 in m2.groups[t-1].members:
            return False
        
        return True

        
    def __canAdd(self,student1: Student, student2: Student, group: Group):

        # check the size condition
        if group.size - self.min_size < 2:
            return False
        
        # for each student check if they already visited the host or has been grouped with any of the members in the former event
        for student in [student1,student2]:

            if student in group.host.studentsThatVisited:
                return False

            for m in group.members:
                if student in m[group.t-1].members:
                    return False
        
        return True

            
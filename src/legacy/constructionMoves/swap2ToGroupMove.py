from typing import List
from src.interfaces import ConstructionMove_base
from src.student import Student
from src.group import Group

class Swap2ToGroupMove(ConstructionMove_base):

    def __init__(self,min_size,max_size) -> None:
        self.max_size = max_size
        self.min_size = min_size

    def performMove(self, group: Group, groups: List[Group]) -> bool:
        """

        """

        if self.max_size - group.size < 2:
            return False

        for g1 in groups:
            if g1 != group:
                for g2 in groups:
                    if g2 != group:
                        for m1, m2 in self.__canRemove(g1,g2):
                            if g1.host == m1:
                                newHost1 = self.__findNewHost(g1)
                                if newHost1 is None:
                                    continue
                            if g2.host == m2:
                                newHost2 = self.__findNewHost(g2)
                                if newHost2 is None:
                                    continue
                            if self.__canAdd(m1,m2,group):
                                if g1.host == m1:
                                    g1.host = newHost1
                                if g2.host == m2:
                                    g2.host = newHost2
                                    
                                g1.removeMember(m1)
                                g2.removeMember(m2)
                                group.addMember(m1)
                                group.addMember(m2)
                                return True
                            

        return False

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
       
    
    def __canRemove(self,group1: Group,group2: Group):
        
        pairs_canRemove = []

        if group1 != group2:

            if group1.size == self.min_size == self.min_size or group2.size == self.min_size:
                return []

            canRemoveGender = {group1: [group1.getGenderCount(0) > 2, group2.getGenderCount(1) > 2], 
                               group2: [group1.getGenderCount(0) > 2, group2.getGenderCount(1) > 2]}
            
            for m1 in group1.members:
                for m2 in group2.members:
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
                for m2 in group1.members:
                    if canRemoveGenderCombination.get((m1.gender,m2.gender)):
                        pairs_canRemove.append((m1,m2))

        return pairs_canRemove

    def __canBeGrouped(self,m1,m2,t):
        
        if m1 in m2.groups[t-1].members:
            return False
        
        return True

        
    def __canAdd(self,student1: Student, student2: Student, group: Group):

        # check the size condition
        if self.max_size - group.size < 2:
            return False
        

        # check gender situation
        if student1.gender != student2.gender:
            if group.getGenderCount(0) == 0 or group.getGenderCount(1) == 0:
                return False

        # for each student check if they already visited the host or has been grouped with any of the members in the former event
        for student in [student1,student2]:

            if student in group.host.studentsThatVisited:
                return False

            for m in group.members:
                if student in m.groups[group.t-1].members:
                    return False
        
        return True

            
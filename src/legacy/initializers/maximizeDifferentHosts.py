from typing import List

import numpy as np
from src.group import Group
from src.interfaces import Initializer_base
from src.student import Student

class MaximizeDifferentHosts_initializer(Initializer_base):

   
    def initializeGroups(self, boys: List[Student], girls: List[Student],num_groups,min_size,t) -> List[Group]:
        #np.random.seed(36)
        np.random.shuffle(boys)
        np.random.shuffle(girls)

        self.groups, remainingBoys, remainingGirls = self.__findHosts(boys, girls, num_groups, t)
            # Add the created group to the list
        
        # assign a person of the same gender as the host
        for group in self.groups:
            if group.host.gender == 1:
                for boy in sorted(remainingBoys,key = lambda x: self.getStudentSortingOrder(x,self.groups)):
                    if self.__canAdd(boy,group,t):
                        group.addMember(boy)
                        remainingBoys.remove(boy)
                        break
            
            else:
                for girl in sorted(remainingGirls,key = lambda x: self.getStudentSortingOrder(x,self.groups)):
                    if self.__canAdd(girl,group,t):
                        group.addMember(girl)
                        remainingGirls.remove(girl)
                        break
        
        # assign opposite gender or same gender 
        for group in self.groups:
            if group.host.gender == 1:
                success = self.__assignOppositeGender(remainingGirls, group, t)
                if not success:
                    self.__assignSameGender(min_size, remainingBoys, group,t)
            else:
                success = self.__assignOppositeGender(remainingBoys, group, t)
                if not success:
                    self.__assignSameGender(min_size, remainingGirls, group,t)

        return self.groups, remainingBoys + remainingGirls 

    def __assignSameGender(self, min_size, remainingStudents, group,t):
        counter = 0
        for student in sorted(remainingStudents,key = lambda x: self.getStudentSortingOrder(x,self.groups)):
            if counter == min_size-2:
                break       
            if self.__canAdd(student,group,t):
                group.addMember(student)
                remainingStudents.remove(student)
                counter +=1

    def __assignOppositeGender(self, remainingStudents, group, t):

        for m1 in sorted(remainingStudents,key = lambda x: self.getStudentSortingOrder(x,self.groups)):
                for m2 in sorted(remainingStudents,key = lambda x: self.getStudentSortingOrder(x,self.groups)):
                    if m1 != m2:
                        if self.__canAdd(m1,group,t) and self.__canAdd(m2,group,t):
                            if self.__canBeGrouped(m1,m2,t):
                                group.addMember(m1)
                                group.addMember(m2)
                                remainingStudents.remove(m1)
                                remainingStudents.remove(m2)
                                return True
        
        return False
            
    
    def __canBeGrouped(self,student1,student2,t):

        if student1 in student2.groups[t-1].members:
            return False

        return True

    def __canAdd(self,student: Student,group: Group,t: int):

        for member in group.members:
            if student in member.groups[t-1].members:
                return False
            if student in group.host.studentsThatVisited:
                return False
        
        return True


    def __findHosts(self, boys, girls, num_groups, t):
        groups = []

        remainingBoys = boys[:]
        remainingGirls = girls[:]

        # Calculate maximum number of boys and girls that can be assigned as hosts
        max_boys_as_hosts = len(boys) // 2
        max_girls_as_hosts = len(girls) // 2

        assert num_groups <= max_boys_as_hosts + max_girls_as_hosts, 'Too few people to be able to create the groups'

        hostPriority = sorted(remainingBoys + remainingGirls, key = lambda x: x.hostTimes)
        
        i = 0
        num_boyHosts = 0
        num_girlHosts = 0
        while len(groups) < num_groups:
            host = hostPriority[i]

            if host.groups[t-1].host == host:
                i += 1
                continue

            # Assign a boy as a host if available and within limits
            if num_boyHosts < max_boys_as_hosts and host.gender == 1:  # Limit the number of boy hosts
                group = Group(host,t)
                num_boyHosts += 1
                groups.append(group)
                remainingBoys.remove(host)

            # Assign a girl as a host if available and within limits
            if num_girlHosts < max_girls_as_hosts and host.gender == 0:  # Limit the number of girl hosts
                group = Group(host,t)
                num_girlHosts += 1
                groups.append(group)
                remainingGirls.remove(host)
            
            i += 1
        return groups,remainingBoys,remainingGirls
    
    def getStudentSortingOrder(self,student,groups):

        counter = len(groups)

        for group in groups:
            if student in group.host.studentsThatVisited:
                counter -= 1
                continue

            for member in group.members:
                if student in member.groups[group.t-1].members:
                    counter -= 1
                    break

        return counter
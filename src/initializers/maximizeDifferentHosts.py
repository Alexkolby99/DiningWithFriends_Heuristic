from typing import List
from src.group import Group
from src.interfaces import Initializer_base
from src.student import Student

class MaximizeDifferentHosts_initializer(Initializer_base):
    def __init__(self, num_groups: int):
        """
        Initializes the HostSelectorInitializer with a specified number of groups.
        
        :param num_groups: The number of groups to create.
        """
        self.num_groups = num_groups

    def initializeGroups(self, boys: List[Student], girls: List[Student],t) -> List[Group]:
        groups = []

        # Calculate maximum number of boys and girls that can be assigned as hosts
        max_boys_as_hosts = len(boys) // 2
        max_girls_as_hosts = len(girls) // 2

        assert self.num_groups <= max_boys_as_hosts + max_girls_as_hosts, 'Too few people to be able to create the groups'

        hostPriority = sorted(boys + girls, key = lambda x: x.hostTimes)
        
        i = 0
        num_boyHosts = 0
        num_girlHosts = 0
        while len(groups) < self.num_groups:
        
            host = hostPriority[i]

            # Assign a boy as a host if available and within limits
            if num_boyHosts < max_boys_as_hosts and host.gender == 1:  # Limit the number of boy hosts
                group = Group(host,t)
                num_boyHosts += 1
                groups.append(group)

            # Assign a girl as a host if available and within limits
            if num_girlHosts < max_girls_as_hosts and host.gender == 0:  # Limit the number of girl hosts
                group = Group(host,t)
                num_girlHosts += 1
                groups.append(group)

            # Add the created group to the list
            i += 1

        return groups
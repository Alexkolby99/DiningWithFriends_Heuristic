from typing import List

from src.group import Group
from src.interfaces import event_Base
from src.student import Student


class Event(event_Base):
    def __init__(self, timestamp: int) -> None:
        self._groups: List[Group] = []
        self._timestamp = timestamp
        self._hosts: List[Student] = []

    @property
    def groups(self) -> List[Group]:
        return self._groups

    @property
    def timeStamp(self) -> int:
        return self._timestamp

    @property
    def hosts(self) -> List[Student]:
        return self._hosts

    def addGroup(self, group: Group) -> None:
        '''Add a group to the event'''
        if group not in self._groups:
            self._groups.append(group)
            for member in group.members:
                member.assignGroup(group)
            group.host.addHostTime()
        else:
            print(f"{group} is already part of the event.")

    def removeGroup(self, group: Group) -> None:
        '''Remove a group from the event'''
        if group in self._groups:
            self._groups.remove(group)
        else:
            print(f"{group} is not part of the event.")

    def addHost(self, host: Student) -> None:
        '''Add a host to the event'''
        if host not in self._hosts:
            self._hosts.append(host)
        else:
            print(f"{host} is already a host of the event.")

    def removeHost(self, host: Student) -> None:
        '''Remove a host from the event'''
        if host in self._hosts:
            self._hosts.remove(host)
        else:
            print(f"{host} is not a host of the event.")

    def __str__(self):

        out_str = f'Event at timestamp {self.timeStamp} has NumberOfGroups = {len(self.groups)}\n'

        for i,g in enumerate(self.groups):
            out_str += f'Group {i} is:\n' 
            out_str += g.__str__()
            out_str += '\n'

        return out_str
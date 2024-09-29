from typing import List, Literal
from src.group import Group
from src.interfaces import student_Base, group_Base

# Concrete implementation of the student_Base interface
class Student(student_Base):
    def __init__(self, identifier: int, gender: Literal[0, 1], num_groups: int) -> None:
        self._identifier = identifier
        self._gender = gender
        self._host_times = 0
        self._students_visited: List[student_Base] = []
        self._groups: List[group_Base] = [Group(None,0)] * num_groups  # Initialize groups with None

    @property
    def identifier(self) -> int:
        return self._identifier
    
    @property
    def gender(self) -> Literal[0, 1]:
        return self._gender

    @property
    def hostTimes(self) -> int:
        return self._host_times

    @property
    def studentsThatVisited(self) -> List[student_Base]:
        return self._students_visited

    @property
    def groups(self) -> List[group_Base]:
        return self._groups

    def addHostTime(self) -> None:
        '''Increment host times by 1'''
        self._host_times += 1

    def removeHostTime(self) -> None:
        '''Subtract one from host times, ensuring it doesn't go below zero'''
        if self._host_times > 0:
            self._host_times -= 1

    def assignGroup(self, group: group_Base) -> None:
        '''Assigns the group at position t in groups'''
        if 0 <= group.t < len(self._groups):
            self._groups[group.t] = group
        else:
            raise IndexError("Group index out of range.")
        
        if group.host == self:
            for member in group.members:
                self.addStudentThatVisited(member)
    
    def addStudentThatVisited(self, student: student_Base) -> None:
        '''Add a student to the visited list'''
        self._students_visited.append(student)
import json
import math
import os
from typing import List

import numpy as np
import pandas as pd
from src.initializers import MaximizeDifferentHosts_initializer
from src.constructionMoves import InsertMove, InsertSwapMove, SwapGroupMove, InsertDoubleSwapMove,Swap2ToGroupMove, InsertWithABuddyMove
from src.student import Student
from src.event import Event

class ConstructionHeuristic:

    def __init__(self,min_size: int,max_size: int,n_events: int) -> None:

        self.min_size = min_size
        self.max_size =  max_size
        self.n_events = n_events
        self.studentMoves = [InsertMove(max_size),InsertSwapMove(max_size),InsertWithABuddyMove(min_size,max_size),InsertDoubleSwapMove(max_size)]
        self.groupMoves = [SwapGroupMove(min_size,max_size),Swap2ToGroupMove(min_size,max_size)]
        self.initializer =  MaximizeDifferentHosts_initializer()
    
    def makeGroupsForOneEvent(self,boys,girls,num_groups,e,m_lower):

        # initialization of the groups
        groups,remainingStudents = self.initializer.initializeGroups(boys,girls,num_groups,self.min_size,e)

        # Assign the remaining students by going through the list of moves
        for move in self.studentMoves:
            for student in sorted(remainingStudents,key = lambda x: self.getStudentSortingOrder(x,groups)):
                success = move.performMove(student,groups)
                if success:
                    remainingStudents.remove(student)
        


        # Try to move students to the group that has too few members by going through the groupMoves
        for g1 in groups:
            if g1.size < self.min_size: 
                for move in self.groupMoves:
                    for _ in range(0,l-g1.size):        
                        success = move.performMove(g1,groups) # can add a move that tries to move two person over, (this allows for moving two girls into a boy only group etc.)
                        if not success: # if not possible to assign a person, no more of this move type will be possible
                            break
        
        for move in self.studentMoves:
            for student in sorted(remainingStudents,key = lambda x: self.getStudentSortingOrder(x,groups)):
                success = move.performMove(student,groups)
                if success:
                    remainingStudents.remove(student)
        
        # Try to break the group up and assign the members to other groups instead if the group is too small
        for g1 in groups[:]:
            if g1.size < self.min_size and len(groups) > m_lower:
                for student in g1.members[:]:
                    for move in self.studentMoves:
                        success = move.performMove(student,groups) # need to make a move that makes a 3 chain swap as well (perhaps also handled swapping with the host in general)
                        if success:
                            g1.removeMember(student)
                            break
            if g1.size == 0:
                groups.remove(g1)

        return groups
        

    def constructSolution(self, n_boys: int, n_girls: int) -> List['Events']:
        """
        Constructs a solution based on the provided boys and girls lists.
        """

        # implement checks for fully feasible solutions
        # e.i If the number of students in the group with most students at an event is larger than the total number of groups then unable to assign all members to new teammates
        # e.i If not enough hosts can be found
        # e.i ..
        m_lower = math.ceil((n_girls+n_boys)/u)
        self.events = [Event(0)]
        num_groups = (n_boys+n_girls) // self.min_size

        boys = [Student(i,1,self.n_events+1) for i in range(n_boys)]
        girls = [Student(i,0,self.n_events+1) for i in range(n_boys,n_boys+n_girls)]

        for e in range(1,self.n_events+1):
            tries = 0
            while tries <= 5:
                groups = self.makeGroupsForOneEvent(boys,girls,num_groups,e,m_lower)

        
                event = Event(e)
                for group in groups:
                    event.addGroup(group)

                if self.__validEvent(event,n_boys+n_girls):
                    self.events.append(event)
                    self.tries = 0
                    break
                else:
                    self.events.append(event)
                    self.tries += 1
                    print(f'Event {e} failed: retrying...')
                    if tries == 5:
                        print('Unable to make the groups')

        return self.events

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
           

    def __validEvent(self,event,numStudents):
        '''
        Method that validates if an event fulfills the requirements
        '''
        timeStamp = event.timeStamp
        totalNumberOfStudents = 0
        
        for idx,_group in  enumerate(event.groups):

            # check the host is in the group
            if _group.host not in _group.members:
                print(f'Error for group {idx}: The host is not in the group')
                return False
            
            totalNumberOfStudents += _group.size

            # Make sure group size fits
            if _group.size > u or _group.size < l:
                print(f'Error for group {idx}: The size of the group does not match')
                return False
            
            # Host Twice in a row
            if _group.host == _group.host.groups[timeStamp-1].host:
                print(f'Error for group {idx}: Host twice in a row')
                return False

            # check validity for members in the group
            genders = np.zeros(2)
            peopleThatVisitTheHost = [[m.identifier for m in g.members if m != _group.host] for g in _group.host.groups[:timeStamp-1] if g.host == _group.host]
            peopleThatVisitTheHost = [item for sublist in peopleThatVisitTheHost for item in sublist]
            for member1 in _group.members:
                genders[member1.gender] += 1
                if member1 in peopleThatVisitTheHost: # if member already visited the host it aint valid
                    print(f'Error for group {idx}: {member1.identifier} already visited the host')
                    return False
            
                for member2 in _group.members:
                    if member1 != member2:
                        if member1 in member2.groups[timeStamp-1].members: # if member was grouped with another member last event aint valid
                            print(f'Error for group {idx}: {member1.identifier} and {member2.identifier} was grouped at last event')
                            return False
            
            # check validity of boys and girls
            if genders[0] == 1 or genders[1] == 1:
                print(f'Error for group {idx}: the gendercount is wrong')
                return False
        
        # check the total number of students
        if totalNumberOfStudents != numStudents:
            print(f'Error for event: All students has not been assigned to a group')
            return False


        return True
    
    def writeToExcel(self,events,filename='overviewFile.xlsx'):
        n_students = sum([g.size for g in events[1].groups])
        M_upper = math.floor((n_students)/l)
        df = pd.DataFrame(index=[f'Group_{i}' for i in range(M_upper)])
        
        for event in events[1:]:
            members = [[m for m in g.members] for g in event.groups]
            hosts = [g.host.identifier for g in event.groups]
            for _ in range(M_upper-len(members)):
                members.append([])
                hosts.append(None)

            df[(f'event {event.timeStamp}','boy members')] = [[m.identifier for m in g if m.gender == 1] for g in members]
            df[(f'event {event.timeStamp}','girl members')] = [[m.identifier for m in g if m.gender == 0] for g in members]
            df[(f'event {event.timeStamp}','Host')] = hosts
        df.columns = pd.MultiIndex.from_tuples(df.columns)
        df.to_excel('overviewFile.xlsx')

if __name__ == '__main__':


    def read_json_to_dict(file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    testInstancefolder = 'testInstances'

    for file in os.listdir(testInstancefolder):
        print(file)
        instance = read_json_to_dict(os.path.join(testInstancefolder,file))
        l = instance['minNumGuests']
        u = instance['maxNumGuests']
        n_boys = instance['n_boys']
        n_girls = instance['n_girls']
        n_events = instance['numOfEvents']
        construction = ConstructionHeuristic(l,u,n_events)
        events = construction.constructSolution(n_boys,n_girls)

    
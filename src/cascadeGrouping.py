import json
import os
import numpy as np
import pandas as pd
from src.student import Student
from src.group import Group
from src.event import Event
from src.constructionMoves import RemoveLonelyGenderMove, SwapLonelyGenderMove, GetSameGenderMove

class CascadeGrouping:


    def __init__(self,n_girls,n_boys,l,u):
        self.n_girls = n_girls
        self.n_boys = n_boys
        self.u = u
        self.l = l
        self.m_lower = int((n_girls+n_boys) // l)
        self.m_upper = int(np.ceil((n_girls+n_boys) / u))


    def constructSolution(self,n_events,validate = True):
        
        events = [Event(0)]

        girls = [Student(i,0,n_events+1) for i in range(self.n_girls)]
        boys = [Student(i,1,n_events+1) for i in range(self.n_girls,self.n_girls+self.n_boys)]

        leastGender = 0  if self.n_girls < self.n_boys else 1

        groupMatrix = self.constructGroupMatrix(girls,boys)
        groups = self.getGroupsFromMatrix(groupMatrix,1)
        for g in groups:
            self.findHosts(g)

        event = Event(1)
        for g in groups:
            event.addGroup(g)
            
        if validate:
            if not self.__validEvent(event):
                raise Exception

        events.append(event)

        eventsSinceCascading =self.m_upper*2+1

        for e in range(2,n_events+1):
            if eventsSinceCascading <= self.m_upper*2:
                groups = self.makeGroupsFromEarlier(events[e-2], e)
                for g in groups:
                    if g.host is None:
                        groups = self.cascadeFormerGroup(leastGender,groupMatrix,e)
            else:
                groups = self.cascadeFormerGroup(leastGender, groupMatrix, e)
                eventsSinceCascading = 0

            event = Event(e)
            for g in groups:
                event.addGroup(g)
                
            if validate:
                if not self.__validEvent(event):
                    raise Exception

            events.append(event)
            eventsSinceCascading += 1

            groupMatrix = self.getMatrixFromGroups(groups,leastGender)

            return events

    def cascadeFormerGroup(self, leastGender, groupMatrix, e):
        groupMatrix = self.cascadeGroupMatrix(groupMatrix)
        groups = self.getGroupsFromMatrix(groupMatrix,e)
        self.repairGenderCount(groups,leastGender)
        
                
        for g in groups:
            _ = self.findHosts(g)

        return groups

    def makeGroupsFromEarlier(self, event,e):
        groups = []
        for oldGroup in event.groups:
            group = Group(None,e)
            for m in oldGroup.members:
                group.addMember(m)
            groups.append(group)

        for g in groups:
            _ = self.findHosts(g)
        
        return groups

    def getMatrixFromGroups(self,groups,leastGender):

        G = np.zeros((self.u,self.m_upper),dtype=Student)
        G[:] = None

        for i in range(self.m_upper):
            leastGender_group = [m for m in groups[i].members if m.gender == leastGender]
            maxGender_group = [m for m in groups[i].members if m.gender != leastGender]

            if len(leastGender_group) == 0:
                G[:len(maxGender_group),i] = maxGender_group
            else:

                G[0,i] = maxGender_group.pop()
                G[1,i] = maxGender_group.pop()
                G[2,i] = leastGender_group.pop()
                G[3,i] = leastGender_group.pop()
                remainingStudents = leastGender_group + maxGender_group
                G[4:4+len(remainingStudents),i] = remainingStudents

        return G

    def constructGroupMatrix(self,girls,boys):
        

        G = np.zeros((self.u,self.m_upper),dtype=Student)


        genderWithMost = girls.copy() if self.n_girls > self.n_boys else boys.copy()
        genderWithLeast = girls.copy() if self.n_girls <= self.n_boys else boys.copy()

        genderWithMost_UniqueGroupCount = min(len(genderWithMost) // 2,self.m_upper)
        genderWithLeast_UniqueGroupCount = min(len(genderWithLeast) // 2,self.m_upper)


        G[0,:genderWithMost_UniqueGroupCount] =genderWithMost [:genderWithMost_UniqueGroupCount]
        G[1,:genderWithMost_UniqueGroupCount] = genderWithMost[genderWithMost_UniqueGroupCount:genderWithMost_UniqueGroupCount*2]

        genderWithMost = genderWithMost[genderWithMost_UniqueGroupCount*2:]

        G[2,:genderWithLeast_UniqueGroupCount] = genderWithLeast[:genderWithLeast_UniqueGroupCount]
        G[3,:genderWithLeast_UniqueGroupCount] = genderWithLeast[genderWithLeast_UniqueGroupCount:genderWithLeast_UniqueGroupCount*2]

        genderWithLeast = genderWithLeast[genderWithLeast_UniqueGroupCount*2:]

        for i in range(self.m_upper)[::-1]:
            if np.count_nonzero(G[:,i]) < 3:     
                G[2,i] = genderWithMost.pop()
                G[3,i] = genderWithMost.pop()
            else:
                break

        for i in range(4,self.u):
            for j in range(self.m_upper):
                if len(genderWithLeast) != 0:
                    G[i,j] = genderWithLeast.pop()
                elif len(genderWithMost) != 0:
                    G[i,j] = genderWithMost.pop()
                else:
                    G[i,j] = None

        return G

    def cascadeGroupMatrix(self,groupMatrix):
        
        G = np.zeros_like(groupMatrix,dtype=Student)

        for i in range(0,self.u)[::-1]:
            offset = self.u-i-1
            G[i,:] = np.concat([groupMatrix[i,-offset:],groupMatrix[i,:-offset]])

        return G

    def getGroupsFromMatrix(self,groupMatrix,t):
        groups = []
        for i in range(self.m_upper):
            group = Group(None,t)
            for m in groupMatrix[:,i]:
                if m is not None:
                    group.addMember(m)
            groups.append(group)

        return groups


    def repairGenderCount(self,groups,leastGender):
        
        # this is where we need to be careful insertmove should check if can be removed from the group as well
        # then there need to be a swap move, that swaps persons

        leastGender_groupCounter = np.array([g.getGenderCount(leastGender) for g in groups if not g.getGenderCount(leastGender) == 0])

        if np.all(leastGender_groupCounter > 1):
                return

        maxIters = 0

        while min(leastGender_groupCounter) < 2 and maxIters < self.m_upper:
            for g in groups:
                if g.getGenderCount(leastGender) == 1:
                    if len(leastGender_groupCounter) > sum(leastGender_groupCounter) // 2:
                        moves =  moves = [RemoveLonelyGenderMove(self.l,self.u),SwapLonelyGenderMove(self.l,self.u)]
                    else:
                        moves = [GetSameGenderMove(self.l,self.u)]
                    for move in moves:
                        status = move.performMove(g,groups)
                        if status == True:
                            leastGender_groupCounter = np.array([g.getGenderCount(leastGender) for g in groups if not g.getGenderCount(leastGender) == 0])
                            break
            
            leastGender_groupCounter = np.array([g.getGenderCount(leastGender) for g in groups if not g.getGenderCount(leastGender) == 0])
            maxIters += 1
        
        assert min(leastGender_groupCounter) >= 2, 'Unable to repair the gender group'


    def findHosts(self,group):
        

        def canHost(member,group):

            if member.groups[group.t-1].host == member:
                return False
            
            for m in group.members:
                if m != member:
                    if m in member.studentsThatVisited:
                        return False            
            return True

        # If possible to find a host do so
        for m in group.members:
            if canHost(m,group):
                group.host = m
                return True

    def writeToExcel(self,events,filename='overviewFile.xlsx'):
        df = pd.DataFrame(index=[f'Group_{i}' for i in range(self.m_upper)])
        
        for event in events[1:]:
            members = [[m for m in g.members] for g in event.groups]
            hosts = [g.host.identifier for g in event.groups]
            for _ in range(self.m_upper-len(members)):
                members.append([])
                hosts.append(None)

            df[(f'event {event.timeStamp}','boy members')] = [[m.identifier for m in g if m.gender == 1] for g in members]
            df[(f'event {event.timeStamp}','girl members')] = [[m.identifier for m in g if m.gender == 0] for g in members]
            df[(f'event {event.timeStamp}','Host')] = hosts
        df.columns = pd.MultiIndex.from_tuples(df.columns)
        df.to_excel(filename)

    def __validEvent(self,event):
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
            if _group.size > self.u or _group.size < self.l:
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
        if totalNumberOfStudents != self.n_boys+self.n_girls:
            print(f'Error for event: All students has not been assigned to a group')
            return False


        return True

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
        grouper = CascadeGrouping(n_girls,n_boys,l,u)
        events = grouper.constructSolution(n_events)

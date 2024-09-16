import math

import numpy as np
from src.event_2 import event
from src.group_2 import group
from src.student_2 import student
from random import shuffle

E = 6
l = 4
u = 5
N_girls = 9
N_boys = 13
N = N_girls+N_boys

girls = [student(i,0,E) for i in range(N_girls)]
boys = [student(i,1,E) for i in range(N_girls,N)]
events = [event(-1)]


def findNewHost(group):

    potentialHosts = [member for member in group]
    for member1 in group:
        for member2 in group:
            if member1 != member2:
                if member2 in member1.studentsThatVisited:
                    potentialHosts.remove(member1)
                    break


    return potentialHosts


def canAdd(members: list[student] | student,group: group):

    if not isinstance(members,list):
        members = [members]

    if group.size + len(members) > u:
        return False


    for gender in [0,1]:
        numberOfGendersToAdd = sum([1 for member in members if member.gender == gender])
        if group.genderCount[gender] < 2-numberOfGendersToAdd and numberOfGendersToAdd + group.genderCount[gender] > 0:
            return False

    # first check that the members to add can be grouped together
    for member1 in members:
        for member2 in members:
            if member1 != member2:
                if member1 in member2.groups[group.timeStamp-1].members or member2 in member1.groups[group.timeStamp-1].members:
                    return False

    # for each member check conditions for a valid group
    for memberToAdd in members:

        # Check that that the member can be assigned to the group
        if memberToAdd in group.invalidOptions:
            return False

        # check that the member to add has not visited the host already
        if memberToAdd in group.host.studentsThatVisited:
            return False
        
        # lastly check that all the group members was not in the member to add at last event
        for member in group.members:
            if member in memberToAdd.groups[group.timeStamp-1].members:
                return False
    
    # if none of the above returns its a valid group
    return True


def canSwap(memberToAdd: student, group: group,t):

    membersThatCanSwapWith = [member for member in group.members if group.host != member] # initial all members can be swapped with


    if group.genderCount[memberToAdd.gender] == 0 or memberToAdd in group.host.studentsThatVisited:
        return []

    # outer loop is the member considered swapping with however you cannot swap with the host
    for member1 in group.members:
        if member1 != group.host:
            for member2 in group.members: # if the member to add does not conflict with any of the remaining in the group, it must only conflict with member1
                if member2 != member1:
                    if group.genderCount[member1.gender] == 2 and member1.gender != memberToAdd.gender:
                        membersThatCanSwapWith.remove(member1)
                        break
                    if memberToAdd in member2.groups[t-1].members:
                        membersThatCanSwapWith.remove(member1)
                        break

    
    return membersThatCanSwapWith

for e in range(1,E+1):
    # step 1 Find host
    _girls = girls.copy()
    _boys = boys.copy()
    #shuffle(_girls)
    #shuffle(_boys)
    students = _girls+_boys
    M = math.floor(N/l)
    hostPriority = sorted(students,key = lambda x: x.hostTimes if x not in events[e-1].hosts else 100) # Handle event 0 somehow here
    groups = []
    girlHosts = 0
    boyHosts = 0
    for i in range(len(hostPriority)):
        if len(groups) < M:
            _host = hostPriority[i]
            if _host.gender == 0 and girlHosts < N_girls/2-1:
                girlHosts += 1
                _girls.remove(_host)
                groups.append(group(e,host=_host))
                continue
            elif _host.gender == 1 and boyHosts < N_boys/2-1:
                boyHosts += 1
                _boys.remove(_host)
                groups.append(group(e,host=_host))
                continue        
            
    # step 2 Assign person of same gender
    for g in groups:
        if  g.host.gender == 0:
            for girl in _girls:
                if girl not in g.host.studentsThatVisited and girl not in g.host.groups[e-1].members: # need to compare options among them
                    g.addMember(girl)
                    _girls.remove(girl)
                    break
            
                
        elif  g.host.gender == 1:
            for boy in _boys:
                if boy not in g.host.studentsThatVisited and boy not in g.host.groups[e-1].members:
                    g.addMember(boy)
                    _boys.remove(boy)
                    break


    # step 2.5: If less than minimum groups is created create a group from pool and swap move

    # step 3 Assign 2 from opposite gender else l-2 from same gender else put in pool

    for g in groups:
        success = False
        if g.host.gender == 0:
            
            # try to assign 2 _boys to the girl group

            for boy1 in _boys:
                if g.size < 4:
                    for boy2 in _boys:
                        if boy1 != boy2 and not success:
                            if canAdd([boy1,boy2],g):
                                g.addMember(boy1)
                                g.addMember(boy2)
                                _boys.remove(boy1)
                                _boys.remove(boy2)
                                success = True
                                break
            
            
            # if not success try to assign l-2 _girls to the group
            if not success:
                girlsToRemove = []
                counter = 0
                for girl in _girls:
                    if counter == l-2:
                        success = True
                        break       
                    if canAdd(girl,g):
                        g.addMember(girl)
                        girlsToRemove.append(girl)
                        counter +=1

                for girl in girlsToRemove:
                    _girls.remove(girl) 
            # # if this does not succeed destroy group and put in pool

            # if not success:
            #     for member in g.members:
            #         _girls.append(member)
                
            #     groups.remove(g)


            
            # try adding two _boys
        elif g.host.gender == 1:
            
            # try to assign 2 _girls to the boy group
            
            for girl1 in _girls:
                if g.size < 4:
                    for girl2 in _girls:
                        if girl1 != girl2 and not success:
                            if canAdd([girl1,girl2],g):
                                g.addMember(girl1)
                                g.addMember(girl2)
                                _girls.remove(girl1)
                                _girls.remove(girl2)
                                success = True
                                break
            
            # if not success try to assign l-2 _girls to the group



            if not success:
                boysToRemove = []
                counter = 0
                for boy in _boys:
                    if counter == l-2:
                        success = True
                        break       
                    if canAdd(boy,g):
                        g.addMember(boy)
                        boysToRemove.append(boy)
                        counter +=1
                    
                for boy in boysToRemove:
                    _boys.remove(boy) 

            # if this does not succeed destroy group and put in pool

            # if not success:
            #     for member in g.members:
            #         _boys.append(member)
                
            #     groups.remove(g)


    # step 4: # if number of groups less than lower bound - need to make a group from the remaining people else try to assign to existing groups

    # step 4.5: Assign remaining one at a time
    girlsToRemove = []
    for girl in _girls:
        for g in groups:
            if canAdd(girl,g) and g.genderCount[0] > 1:
                g.addMember(girl)
                girlsToRemove.append(girl)
                break
    for girl in girlsToRemove:
        _girls.remove(girl)

    boysToRemove = []
    for boy in _boys:
        for g in groups:
            if canAdd(boy,g) and g.genderCount[0] > 1:
                g.addMember(boy)
                boysToRemove.append(boy)
                break
                
    for boy in boysToRemove:
        _boys.remove(boy)

    # step 5 Perform moves to get feasible solution


        
    #     # find Persons That can join there group

    for g1 in groups:
        for g2 in groups:
            if g1 != g2 and g1.size < l and g2.size > l:
                for member in g2.members:
                    if g2.host != member and g2.genderCount[member.gender] > 2 and g1.genderCount[member.gender] > 1:
                        if canAdd(member,g1):
                            g2.removeMember(member)
                            g1.addMember(member)
                            if g1.size >= l:
                                break

    girlsToRemove = []
    for girl in _girls:
        for g in groups:
            if canAdd(girl,g) and g.genderCount[0] > 1:
                g.addMember(girl)
                girlsToRemove.append(girl)
                break
    for girl in girlsToRemove:
        _girls.remove(girl)

    boysToRemove = []
    for boy in _boys:
        for g in groups:
            if canAdd(boy,g) and g.genderCount[0] > 1:
                g.addMember(boy)
                boysToRemove.append(boy)
                break
                
    for boy in boysToRemove:
        _boys.remove(boy)
    # # insert-swap move

    boysToRemove = []
    for i in range(len(_boys)):
        success = False
        boy = _boys[i]
        for g in groups:
            if success:
                break
            for member in canSwap(boy,g,e):
                if not success:
                    for g2 in groups:
                        if canAdd(member,g2):
                            g.removeMember(member)
                            g.addMember(boy)
                            g2.addMember(member)
                            boysToRemove.append(boy)
                            success = True
                            break
    
    for boy in boysToRemove:
        _boys.remove(boy)

    girlsToRemove = []
    for i in range(len(_girls)):
        success = False
        girl = _girls[i]
        for g in groups:
            if success:
                break
            for member in canSwap(girl,g,e):
                if not success:
                    for g2 in groups:
                        if canAdd(member,g2):
                            g.removeMember(member)
                            g.addMember(girl)
                            g2.addMember(member)
                            girlsToRemove.append(girl)
                            success = True

    for girl in girlsToRemove:
        _girls.remove(girl)
    # insert-swap host move




    # insert and remove 2 persons from group


    # lastly should create event with given groups and update accordingly

    _event = event(e)
    _event.addGroups(groups)
    events.append(_event)

## validation

for idx,_event in enumerate(events[2:]):
    idx += 1
    totalNumberOfStudents = 0
    
    for _group in  _event.groups:
        totalNumberOfStudents += _group.size


        # Make sure group size fits
        if _group.size > u or _group.size < l:
            raise ValueError
        
        # Host Twice in a row
        if _group.host == _group.host.groups[idx].host:
            raise ValueError

        # check validity for members in the group
        genders = np.zeros(2)
        for member1 in _group.members:
            genders[member1.gender] += 1
            if member1 in _group.host.studentsThatVisited: # if member already visited the host it aint valid
                raise ValueError
            for member2 in _group.members:
                if member1 != member2:
                    if member1 in member2.groups[idx].members: # if member was grouped with another member last event aint valid
                        raise ValueError
        
        # check validity of boys and girls
        if genders[0] == 1 or genders[1] == 1:
            raise ValueError
    
    # check the total number of students
    if totalNumberOfStudents != N_girls + N_boys:
        raise ValueError

pass
            
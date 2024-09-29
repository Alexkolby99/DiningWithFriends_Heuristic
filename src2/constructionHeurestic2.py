import math

import numpy as np
import pandas as pd
from src.event_2 import event
from src.group_2 import group
from src.student_2 import student




def constructionHeurestic(E,l,u,N_girls,N_boys):

    N = N_girls+N_boys
    girls = [student(i,0,E) for i in range(N_girls)]
    boys = [student(i,1,E) for i in range(N_girls,N)]
    events = [event(-1)]

    def possibleHosts(group: group,removeCurrentHost = True):

        possibleHosts = [m for m in group.members]
        if removeCurrentHost:
            possibleHosts.remove(group.host)
        for m1 in group.members:
            if m1.groups[e-1].host == m1:
                possibleHosts.remove(m1)
                continue
            if m1 != group.host:
                for m2 in group.members:
                    if m1 != m2 and m2 != group.host:
                        if m2 in m1.studentsThatVisited:
                            possibleHosts.remove(m1)
                            break

        return possibleHosts

    def canRemove(group: group):

        if group.size == l:
            return []

        membersThatCanBeRemoved = [member for member in group.members if member != group.host]

        membersThatCanBeRemoved.append(group.host)

        

        for member in group.members:
            if group.host == member:
                if len(possibleHosts(group)) == 0:
                    membersThatCanBeRemoved.remove(member)

            elif group.genderCount[member.gender] <= 2:
                membersThatCanBeRemoved.remove(member)
            
        return membersThatCanBeRemoved

    def canAdd(members: list[student] | student,group: group,exclude: list[student]=None):

        

        if not isinstance(members,list):
            members = [members]

        numberOfAddedMembers = len(members) if exclude is None else len(members)-len(exclude)

        if group.size + numberOfAddedMembers > u:
            return False

        for gender in [0,1]:
            numberOfGendersRemoved = sum([1 for m in exclude if m.gender == gender]) if exclude is not None else 0
            numberOfGendersToAdd = sum([1 for member in members if member.gender == gender]) - numberOfGendersRemoved
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
                if exclude is not None:
                    if member in exclude:
                        continue
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
        M_upper = math.floor(N/l)
        M_lower = math.floor(N/u)
        hostPriority = sorted(students,key = lambda x: x.hostTimes if x not in events[e-1].hosts else 100) # Handle event 0 somehow here
        groups = []
        girlHosts = 0
        boyHosts = 0

        # step 1 assign hosts to M_upper groups
        for i in range(len(hostPriority)):
            if len(groups) < M_upper:
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
                
        # step 2 Assign person of same gender as the host to each group
        for idx,g in enumerate(groups):
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


        # step 3 Assign 2 from opposite gender else l-2 from same gender else put in pool

        for g in groups:
            success = False
            if g.host.gender == 0:
                
                # try to assign 2 _boys to the girl group

                for boy1 in sorted(_boys,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
                    if g.size < 4:
                        for boy2 in sorted(_boys,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
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
                
                for girl1 in sorted(_girls,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
                    if g.size < 4:
                        for girl2 in sorted(_girls,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
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

        # step 4: insert-move
        girlsToRemove = []

        for girl in sorted(_girls,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
            for g in groups:
                if canAdd(girl,g) and g.genderCount[0] > 1:
                    g.addMember(girl)
                    _girls.remove(girl)
                    break
        
        if len(_girls) != 0:
            for girl in _girls[:]:
                success = False
                for g1 in groups:
                    if success:
                        break
                    for m in canSwap(girl,g1,e):
                        if success:
                            break
                        for g2 in groups:
                            if g2 != g1:
                                if canAdd(m,g2):
                                    g1.removeMember(m)
                                    g2.addMember(m)
                                    g1.addMember(girl)
                                    _girls.remove(girl)
                                    success = True
                                    break

        for boy in sorted(_boys,key=lambda b: sum([b not in g.invalidOptions for g in groups])):
            for g in groups:
                if canAdd(boy,g) and g.genderCount[0] > 1:
                    g.addMember(boy)
                    _boys.remove(boy)
                    break

        
        if len(_boys) != 0:
            for boy in _boys[:]:
                success = False
                for g1 in groups:
                    if success:
                        break
                    for m in canSwap(boy,g1,e):
                        if success:
                            break
                        for g2 in groups:
                            if g2 != g1:
                                if canAdd(m,g2):
                                    g1.removeMember(m)
                                    g2.addMember(m)
                                    g1.addMember(boy)
                                    _boys.remove(boy)
                                    success = True
                                    break
  
        

        # step 5 Perform moves to get feasible solution

        
        #     # find Persons That can join there group

        # for groups with less than l people, try to find members that can be added
        # Remove-Insert-Move
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
        # insert-move
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


        # handled groups with less than l size by destroying it

        for g1 in groups[:]:
            if g1.size < l and len(groups) > M_lower:
                for m1 in g1.members[:]:
                    success = False
                    # simple insert into another group move
                    for g2 in groups:
                        if g2 != g1:
                            if canAdd(m1,g2):
                                g1.removeMember(m1)
                                g2.addMember(m1)
                                success = True
                                break

                    if not success:
                        for g2 in groups:
                            if success:
                                break
                            if g2 != g1:
                                # more tricky swap-insert move
                                for m2 in canSwap(m1,g2,e):
                                    if success:
                                        break
                                    for g3 in groups:
                                        if g3 != g2 and g3 != g1:
                                            if canAdd(m2,g3) and g3.genderCount[m2.gender] != 0:
                                                g2.removeMember(m2)
                                                g3.addMember(m2)
                                                g1.removeMember(m1)
                                                g2.addMember(m1) 
                                                success = True
                                                break

                    if not success:
                        for g2 in groups:
                            if success:
                                break
                            if g2 != g1:
                                # more tricky double-swap-insert move
                                for m2 in canSwap(m1,g2,e):
                                    if success:
                                        break
                                    for g3 in groups:
                                        if success:
                                            break
                                        for m3 in canSwap(m2,g3,e):
                                            if success:
                                                break
                                            for g4 in groups:
                                                if g4 != g1 and g4 != g3:
                                                    if canAdd(m3,g4) and g4.genderCount[m3.gender] != 0 and g3.genderCount[m2.gender] != 0:
                                                        g2.removeMember(m2)
                                                        g3.addMember(m2)
                                                        g1.removeMember(m1)
                                                        g2.addMember(m1) 
                                                        g3.removeMember(m3)
                                                        g4.addMember(m3)
                                                        success = True
                                                        break     
                    if g1.size == 0:
                        groups.remove(g1)    
                                    

                                

        # if not succesfully to insert the destroyed groups attempt to repair them by a swap and insert move (gets a bit tricky due to the hosts are allowed to swap as well)

        for g1 in groups:
            if g1.size < l:
                for g2 in groups:   
                    if g2 != g1 and g1.size < l:
                        for m1 in g2.members:
                            reset = False
                            if g1.size < l:
                                if canAdd(m1,g1):
                                    if g2.host == m1:
                                        hostOptions2 = possibleHosts(g2)
                                        if hostOptions2 == 0:
                                            continue
                                    for g3 in groups:
                                        if reset:
                                            break
                                        if g3 != g2 and g3 != g1 and g3.size > l and g1.size < l:
                                            for m2 in canRemove(g3):
                                                if canAdd(m2,g2,exclude=[m1]):
                                                    if g2.host == m1:
                                                        for option in hostOptions2:
                                                            failed = True
                                                            if m2 not in option.groups[e-1].members:
                                                                g2.host = option
                                                                failed = False
                                                                break

                                                        if failed:
                                                            continue

                                                    if g3.host == m2:
                                                        hostOptions3 = possibleHosts(g3)
                                                        g3.host = hostOptions3[0]

                                                    g1.addMember(m1)
                                                    g2.removeMember(m1)
                                                    g2.addMember(m2)
                                                    g3.removeMember(m2)
                                                    reset = True
                                                    break

        _event = event(e)
        _event.addGroups(groups)
        events.append(_event)

    ## validation

    for idx,_event in enumerate(events[2:]):
        idx += 1
        totalNumberOfStudents = 0
        
        for _group in  _event.groups:

            # check the host is in the group
            if _group.host not in _group.members:
                raise ValueError
            
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
                visitedUpUntilNow = [[m.identifier for m in g.members if m != _group.host] for g in _group.host.groups[:idx] if g.host == _group.host]
                if member1 in [item for sublist in visitedUpUntilNow for item in sublist]: # if member already visited the host it aint valid
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


    return events


E = 15
l = 12
u = 15
N_girls = 123
N_boys = 100
M_upper = math.floor((N_girls+N_boys)/l)

def toExcel(events):

    df = pd.DataFrame(index=[f'Group_{i}' for i in range(M_upper)])

    for event in events[1:]:
        members = [[m for m in g.members] for g in event.groups]
        hosts = [g.host.identifier for g in event.groups]
        for _ in range(M_upper-len(members)):
            members.append([])
            hosts.append(None)

        df[(f'event {event.timestamp}','boy members')] = [[m.identifier for m in g if m.gender == 1] for g in members]
        df[(f'event {event.timestamp}','girl members')] = [[m.identifier for m in g if m.gender == 0] for g in members]
        df[(f'event {event.timestamp}','Host')] = hosts
    df.columns = pd.MultiIndex.from_tuples(df.columns)
    df.to_excel('overviewFile.xlsx')
    pass


for _ in range(100):

    N_girls = np.random.randint(10,200)
    N_boys = N_girls + np.random.randint(-20,20)
    l = np.random.randint(4,min(int((N_girls+N_boys)/2),10))
    u = np.random.randint(l+1,l+3)
    E = np.random.randint(0,min(int((N_girls+N_boys)/3),22))

    try:
        events = constructionHeurestic(E,l,u,N_girls,N_boys)
    except Exception as e:
        pass

toExcel(events)
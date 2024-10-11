import numpy as np
from src.group import Group
from src.student import Student
from src.event import Event

def makeGroupMatrix(groups):

    # might need to do some sorting on the gender

    u = max(groups, key = lambda x: x.size).size

    G = np.array([[g.members[i] if i < len(g.members) else None for i in range(u)] for g in groups]).T

    return G

def makeGroupsFromMatrix(GroupMatrix,t):
    groups = []
    for i in range(GroupMatrix.shape[1]):
        group = Group(None,t)
        for m in GroupMatrix[:,i]:
            if m is not None:
                group.addMember(m)
        groups.append(group)

    return groups

def makeGroupsFromFormer(groups,boys,girls,t):
    


    def fixGenderCount(group):

        # does not work need to handle how i can access the current group of all students

        if group.getGenderCount(0) == 1:
            for girl in girls:
                if girl.groups[t] != group:
                    if girl.groups[t].getGenderCount(1) > 2:
                        for boy in group.members:
                            if boy.gender == 0:
                                if canSwap(boy,girl):
                                    girl.groups[t].addMember(boy)
                                    group.removeMember(boy)
                                    girl.groups[t].removeMember(girl)
                                    group.addMember(girl)
                                    return
                            
            for boy in group.members:
                if boy.gender == 0:
                    for girl in girls:
                        if girl.groups[t] != boy.groups[t]:
                            if girl.groups[t].getGenderCount(1) != 2 and girl.groups[t].getGenderCount(0) > 0:
                                if canSwap(girl,boy):
                                    group.removeMember(boy)
                                    group.addMember(girl)
                                    girl.groups[t].addMember(boy)
                                    girl.groups[t].removeMember(girl)
                                    return


        if group.getGenderCount(1) == 1:
            for boy in boys:
                if boy.groups[t] != group:
                    if boy.groups[t].getGenderCount(0) > 2:
                        for girl in group.members:
                            if girl.gender == 1:
                                if canSwap(boy,girl):
                                    boy.groups[t].addMember(girl)
                                    group.removeMember(girl)
                                    boy.groups[t].removeMember(boy)
                                    group.addMember(boy)
                                    return
                            
            for girl in group.members:
                if girl.gender == 1:
                    for boy in boys:
                        if boy.groups[t] != girl.groups[t]:
                            if boy.groups[t].getGenderCount(1) != 2 and boy.groups[t].getGenderCount(0) > 0:
                                if canSwap(girl,boy):
                                    group.removeMember(girl)
                                    group.addMember(boy)
                                    boy.groups[t].addMember(girl)
                                    boy.groups[t].removeMember(boy)
                                    return
        
    groupMatrix = makeGroupMatrix(groups)
    G = np.zeros_like(groupMatrix)

    u, n_groups = groupMatrix.shape 

    for i in range(0,u)[::-1]:
        offset = u-i-1
        G[i,:] = np.concat([groupMatrix[i,-offset:],groupMatrix[i,:-offset]])

    groups = makeGroupsFromMatrix(G,t)

    for group in groups:
        fixGenderCount(group)
        # might need to do more here

    return groups

def canHost(student,group):

    if student.groups[group.t-1].host == student:
        return False
    
    for m2 in groups:
        if m2 in student.studentsThatVisited:
            return False  
    return True

def canSwap(m1,m2,t):

    for _m in m1.groups[t]:
        if _m != m1:
            if _m in m2.groups[t-1]:
                return False
            
    for _m in m2.groups[t]:
        if _m != m2:
            if _m in m1.groups[t-1]:
                return False
            
    return True


def canAdd(student: Student,group: Group,u):

    if group.size == u:
        return False

    if group.host is not None:
        if student in group.host.studentsThatVisited:
            return False

    if group.getGenderCount(student.gender) == 0:
        return False

    for member in group.members:
        if student in member.groups[group.t-1].members:
            return False

    return True

def makeGroups(n_boys,n_girls,u,l,T):

    n_students = n_boys+n_girls

    boys = [Student(i,0,T+1) for i in range(n_boys)]
    girls = [Student(i,1,T+1) for i in range(n_boys,n_students)]

    _boys = boys.copy()
    _girls = girls.copy()
    n_groups = n_students // l
    events = [None for _ in range(n_groups)]
    groups = [Group(None,1) for _ in range(n_groups)]

    # Setup group at first event, that is as even as possible when considering the number of girls, boys in the group
    i = 0
    while i < n_groups:
        if len(_boys) > 1:
            groups[i].addMember(_boys.pop())
            groups[i].addMember(_boys.pop())
        if len(_girls) > 1:
            groups[i].addMember(_girls.pop())
            groups[i].addMember(_girls.pop())
        i += 1

    # might need to handle how 

    for group in sorted(groups,key=lambda x: x.size):
        if len(_boys) + len(_girls) > 0:
            while group.size < l:
                for m in _boys[:]:
                    if canAdd(m,group,u):
                        group.addMember(m)
                        _boys.remove(m)
                        if group.size == l:
                            break

                if group.size != l:
                    for m in _girls[:]:
                        if canAdd(m,group):
                            group.addMember(m)
                            _girls.remove(m)
                            if group.size == l:
                                break

    for m in _boys[:]:
        for g in groups:
            if canAdd(m,g,u):
                g.addMember(m)
                _boys.remove(m)
                break

    for m in _girls[:]:
        for g in groups:
            if canAdd(m,g,u):
                g.addMember(m)
                _girls.remove(m)
                break
    
    event = Event(1)

    for group in groups:
        group.host = group.members[0] # since first event any can be the host
        event.addGroup(group)

    events[1] = event
    

    # Iterate over the remaining events 
    counterSinceNewGroupFormation = 10000
    for t in range(2,T+1):
        event = Event(t)
        if counterSinceNewGroupFormation >= l*2:
            newGroups = makeGroupsFromFormer(groups,boys,girls,t)

            # Host Assignment
            for group in newGroups:
                for m in group.members:
                    if canHost(m,group):
                        group.host = m
                        break
            
            # handle groups unable to get a host
            for group in newGroups:
                if group.host is None:
                    pass # some move

            for group in newGroups:
                event.addGroup(group)

            counterSinceNewGroupFormation = 0
        else:
            newGroups = events[t-1].groups
            for group in newGroups:
                group.host = None
            
                        # Host Assignment
            for group in newGroups:
                for m in group.members:
                    if canHost(m,group):
                        group.host = m
                        break
            
            # handle groups unable to get a host
            for group in newGroups:
                if group.host is None:
                    pass # some move

            for group in newGroups:
                event.addGroup(group)

            counterSinceNewGroupFormation += 1

        groups = newGroups
        events[t] = event

    return events
    
        


if __name__ == '__main__':
    makeGroups(16,11,5,4,8)

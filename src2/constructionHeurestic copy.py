from src import group, student
import numpy as np


T = 3
N = 11
group1v2 = [0,0,0,0,0,0,1,1,1,1,1]

alpha = np.zeros((N,N))
beta = np.zeros((T,N))
y = np.zeros((T,N,N))

types = {'boys':0,'girls':1}

students = [student(group1v2[i],i,T,N) for i in range(N)]

for t in range(T):
    groups = [group(N,t)]
    for type in ['boys','girls']:
        _type = types.get(type)
        students_type = [s for s in students if s.type ==_type]
        for s in students_type:
            addedToAGroup = False
            for _group in groups:
                if _group.size < 2:
                    try:
                        _group.addMember(s)
                        addedToAGroup = True
                        break
                    except AssertionError:
                        continue

            if not addedToAGroup:
                newGroup = group(N,t)
                newGroup.addMember(s)
                groups.append(newGroup)
                         


        

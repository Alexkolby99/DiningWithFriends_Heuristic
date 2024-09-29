import random
from src import group, student
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')

T = 1
N = 13
preGroup = [0,0,0,0,0,0,0,1,1,1,1,1,1]
groupSize_min = 3
groupSize_max = 4

alpha = np.zeros((N,N))
beta = np.zeros((T,N))
y = np.zeros((T,N,N))

types = {'boys':0,'girls':1}

students = [student(preGroup[i],i,T,N) for i in range(N)]
groups = []
G = nx.Graph()

### step 1 pair boys in groups for themselves and girls in groups for themselves before trying to merge those groups

for t in range(T):
    for s in students:
        student_group = group(N,t,preGroup,groupSize_min,groupSize_max)
        student_group.addMember(s)
        G.add_node(student_group)

    while not all([node.validSize for node in G.nodes]):
        for node1 in G.nodes:
            for node2 in G.nodes:
                if node1.canMerge(node2):
                    G.add_edge(node1,node2)

        nodesToChooseFrom = [node for node in list(G.nodes) if not node.validSize]
        while True:
            if len(nodesToChooseFrom)==0:
                break
            
            node = min(nodesToChooseFrom,key=lambda x: G.degree(x))
            nodeToMergeWith = min(G.edges(node),key = lambda x: x[1].size)[1]     

            nodesToChooseFrom.remove(node)   
            G.remove_node(node)
            for member in node.members:
                nodeToMergeWith.addMember(member)

            if nodeToMergeWith in nodesToChooseFrom:
                nodesToChooseFrom.remove(nodeToMergeWith)
    
        G = nx.create_empty_copy(G)
 
    # hostAssignment

    pass
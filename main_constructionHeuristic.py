from src.cascadeGrouping import CascadeGrouping

# The actual data for the problem
n_girls = 8
n_boys = 8
n_events = 3  
l = 4
u = 4

if __name__ == '__main__':
    constructionHeurstic = CascadeGrouping(n_girls,n_boys,l,u)
    events = constructionHeurstic.constructSolution(n_events)
    for event in events[1:]:
        print(event)
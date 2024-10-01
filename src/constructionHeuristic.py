from typing import List
from src.initializers import MaximizeDifferentHosts_initializer
from src.constructionMoves import InsertMove, InsertSwapMove, SwapGroupMove
from src.student import Student
from src.event import Event

class ConstructionHeuristic:

    def __init__(self) -> None:

        self.initializer =  MaximizeDifferentHosts_initializer()
    
        

    def constructSolution(self, n_boys: int, n_girls: int,min_size: int, max_size:int,n_events) -> List['Events']:
        """
        Constructs a solution based on the provided boys and girls lists.
        """
        self.studentMoves = [InsertMove(max_size),InsertSwapMove(max_size)]
        self.groupMoves = [SwapGroupMove(max_size)]
        self.events = [Event(-1)]
        num_groups = (n_boys+n_girls) // min_size

        boys = [Student(i,1,n_events+1) for i in range(n_boys)]
        girls = [Student(i,0,n_events+1) for i in range(n_boys,n_boys+n_girls)]

        for e in range(1,n_events+1):
            

            # initialization of the groups
            groups,remainingStudents = self.initializer.initializeGroups(boys,girls,num_groups,min_size,e)

            # Assign the remaining students by going through the list of moves
            for move in self.studentMoves:
                for student in remainingStudents[:]:
                    success = move.performMove(student,groups)
                    if success:
                        remainingStudents.remove(student)
            


            # Try to move students to the group that has too few members by going through the groupMoves
            for g1 in groups:
                if group.size < min_size: 
                    for move in self.groupMoves:
                        for _ in range(0,l-g1.size):        
                            success = move.performMove(group,groups) # can add a move that tries to move two person over, (this allows for moving two girls into a boy only group etc.)
                            if not success: # if not possible to assign a person, no more of this move type will be possible
                                break

            
            # Try to break the group up and assign the members to other groups instead if the group is too small
            for g1 in groups:
                if group.size < min_size:
                    for student in g1.members[:]:
                        for move in self.studentMoves:
                            success = move.performMove(student,groups) # need to make a move that makes a 3 chain swap as well (perhaps also handled swapping with the host in general)
                            if success:
                                g1.removeMember(student)
                                break

            
        
            event = Event(e)
            for group in groups:
                event.addGroup(group)

            if self.validEvent(event):
                self.events.append(event)
            else:
                raise ValueError


    def validEvent(self,event):
        '''
        Method that validates if an event fulfills the requirements
        '''
        return True
if __name__ == '__main__':


    
    construction = ConstructionHeuristic()
    u = 4
    l = 5
    n_boys = 13
    n_girls = 9
    construction.constructSolution(n_boys,n_girls,u,l,2)

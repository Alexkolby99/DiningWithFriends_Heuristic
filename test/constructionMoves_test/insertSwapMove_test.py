
import unittest
from src.student import Student
from src.group import Group
from src.constructionMoves import InsertSwapMove

class TestinsertSwapMove(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.move = InsertSwapMove(2)
        self.student = Student(identifier=0,gender=1,num_groups=3)
    

    ## TEST LIST
    # If unable to swap between g1 and g2 no insert move can happen
    # If No one can swap with student from g1 then unable to perform the move
    # Cannot make a move if the size of g1 and g2 are max size
    # Otherwise a move should be able to be made

    def testCannotInsertIfG1MembersCanNotJoinG2(self):
        host1 = Student(1,1,3)
        host2 = Student(2,0,3)
        m1 = Student(3,1,3)
        g1 = Group(host1,1)
        g2 = Group(host2,1)
        g1.addMember(m1)
        
        groups = [g1,g2]

        self.assertFalse(self.move.performMove(self.student,groups))

    def testCannotInsertStudentIfNoOneCanSwapWithHimInG1(self):
        host1 = Student(1,0,3)
        m1 = Student(3,0,3)
        host2 = Student(2,1,3)
        g1 = Group(host1,1) # group 1 is two girls can hence not swap any of the girls out
        g2 = Group(host2,1)
        g1.addMember(m1)

        groups = [g1,g2]
        self.assertFalse(self.move.performMove(self.student,groups))

    def testCannotMakeMoveIfG1andG2AreBothFull(self):
        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        host2 = Student(2,1,3)
        m2 = Student(4,1,3)
        g1 = Group(host1,1) # group 1 is two girls can hence not swap any of the girls out
        g2 = Group(host2,1)
        g1.addMember(m1)
        g2.addMember(m2)

        groups = [g1,g2]
        self.assertFalse(self.move.performMove(self.student,groups))

    def testShouldBeAbleToMakeMoveOtherWise(self):
        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        host2 = Student(2,1,3)
        g1 = Group(host1,1) 
        g2 = Group(host2,1)
        g1.addMember(m1)

        groups = [g2,g1]
        self.assertTrue(self.move.performMove(self.student,groups))

        self.assertIn(m1,g2.members)
        self.assertNotIn(m1,g1.members)
        self.assertIn(self.student,g1.members)
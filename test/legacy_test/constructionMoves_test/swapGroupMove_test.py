
import unittest
from src.student import Student
from src.group import Group
from src.constructionMoves import SwapGroupMove

class TestSwapGroupMove(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.move = SwapGroupMove(2,3)
        host = Student(0,0,3)
        self.group = Group(host,1)

    # If no one can be removed from a group no move can be made
    # If unable to add with the students in the group no move should happen
    # If able to remove someone and add them a move should be made

    def testCannotDoIfNoOneCanBeRemoved(self):
        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        
        groups = [self.group,g1]

        self.assertFalse(self.move.performMove(self.group,groups))


    def testCannotDoIfCannotAdd(self):
        
        host1 = Student(1,1,3)
        m1 = Student(2,1,3)
        m2 = Student(3,1,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        g1.addMember(m2)
        
        groups = [self.group,g1]

        self.assertFalse(self.move.performMove(self.group,groups))

    
    def testCanDoIfCanRemoveAndCanAdd(self):

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        m2 = Student(3,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        g1.addMember(m2)
        
        host2 = Student(5,1,3)
        m3 = Student(4,1,3)
        g2 = Group(host2,1)
        g2.addMember(m3)

        groups = [self.group,g2,g1]

        self.assertTrue(self.move.performMove(self.group,groups))

        self.assertIn(m1,self.group.members)
        self.assertNotIn(m1,g1.members)
        
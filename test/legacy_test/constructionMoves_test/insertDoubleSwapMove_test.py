
import unittest
from src.student import Student
from src.group import Group
from src.constructionMoves import InsertDoubleSwapMove

class TestinsertSwapMove(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.move = InsertDoubleSwapMove(2)
        self.student = Student(identifier=0,gender=1,num_groups=3)
    

    ## TEST LIST
    # Cannot insert if g1 members cannot join g2 
    # Cannot insert if g2 members cannot join g3
    # can insert if m1 can join g2 and m2 can join g3
    # can insert if m1 can join g2 and m2 can join g3 where g3 is g2 

    def testCannotInsertIfG1MembersCanNotJoinG2(self):
        
        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        g1 = Group(host1,1)
        g1.addMember(m1)     

        host2 = Student(2,0,3)
        m2 = Student(4,0,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        
        host3 = Student(5,0,3)
        g3 = Group(host3,1)
        
        groups = [g1,g2,g3]

        self.assertFalse(self.move.performMove(self.student,groups))
        self.assertIn(m1,g1.members)
        self.assertIn(m2,g2.members)

    def testCannotInsertIfG2MembersCanNotJoinG3(self):
        
        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        g1 = Group(host1,1)
        g1.addMember(m1)     

        host2 = Student(2,1,3)
        m2 = Student(4,1,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        
        host3 = Student(5,0,3)
        g3 = Group(host3,1)
        
        groups = [g1,g2,g3]

        self.assertFalse(self.move.performMove(self.student,groups))
        self.assertIn(m1,g1.members)
        self.assertIn(m2,g2.members)

    def testCanInsertIfm1CanJoinG2andM2CanJoinG3(self):
        
        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        g1 = Group(host1,1)
        g1.addMember(m1)     

        host2 = Student(2,1,3)
        m2 = Student(4,1,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        
        host3 = Student(5,1,3)
        g3 = Group(host3,1)
        
        groups = [g1,g2,g3]

        self.assertTrue(self.move.performMove(self.student,groups))
        self.assertIn(self.student,g1.members)
        self.assertIn(m1,g2.members)
        self.assertIn(m2,g3.members)

    def testCanInsertIfm1CanJoinG2andM2CanJoinG3AndG2andG3TheSame(self):
        
        move = InsertDoubleSwapMove(3)

        host1 = Student(1,1,3)
        m1 = Student(3,1,3)
        g1 = Group(host1,2)
        g1.addMember(m1)     

        host2 = Student(2,1,3)
        m2 = Student(4,1,3)
        m3 = Student(5,1,3)
        g2 = Group(host2,2)
        g2.addMember(m2)
        g2.addMember(m3)
        
        formerHost = Student(6,1,3)

        formerGroup = Group(formerHost,1)
        formerGroup.addMember(m1)
        formerGroup.addMember(self.student)

        self.student.assignGroup(formerGroup)
        m1.assignGroup(formerGroup)

        groups = [g1,g2]

        self.assertTrue(move.performMove(self.student,groups))
        self.assertIn(self.student,g1.members)
        self.assertIn(m1,g2.members)
        self.assertIn(m2,g1.members)

  

import unittest
from src.student import Student
from src.group import Group
from src.constructionMoves import Swap2ToGroupMove

class TestSwapGroupMove(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.move = Swap2ToGroupMove(2,3)
        host = Student(0,0,3)
        self.group = Group(host,1)


    ## TESTLIST
    # test cannot swap if cannot remove any
    # test cannot swap if there is only space for one in self.group
    # test cannot swap if can only remove 1
    # test cannot swap if can not insert both in the group
    # test cannot swap if m1 and m2 cannot be grouped together
    # test can swap if 2 from different groups can be removed and both can be inserted
    # test can swap if 2 from same group can be removed and both can be inserted

    
    def test_cannotSwapIfNoOneCanBeRemove(self):

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)

        host2 = Student(3,0,3)
        m2 = Student(4,0,3)
        g2 = Group(host2,1)
        g2.addMember(m2)

        groups = [self.group,g1,g2]

        self.assertFalse(self.move.performMove(self.group,groups))
    

    def test_cannotSwapIfOnlyRoomForOneInGroup(self):

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)

        host2 = Student(3,0,3)
        m2 = Student(4,0,3)
        g2 = Group(host2,1)
        self.group.addMember(m2)

        groups = [self.group,g1,g2]

        self.assertFalse(self.move.performMove(self.group,groups))

    
    def test_cannotSwapIfOnlyOneCanBeRemoved(self):

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)

        host2 = Student(3,0,3)
        m2 = Student(4,0,3)
        m3 = Student(5,0,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        g2.addMember(m3)

        groups = [self.group,g1,g2]

        self.assertFalse(self.move.performMove(self.group,groups))
    
    def test_cannotSwapIfOnlyOneCanBeMovedToThGroup(self):

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        m4 = Student(6,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        g1.addMember(m4)

        host2 = Student(3,1,3)
        m2 = Student(4,1,3)
        m3 = Student(5,1,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        g2.addMember(m3)
        
        groups = [self.group,g1,g2]

        self.assertFalse(self.move.performMove(self.group,groups))

    def test_cannotSwapIfM1andM2cannotBeGrouped(self):

        host = Student(0,1,3)
        self.group = Group(host,2)

        host1 = Student(1,1,3)
        m1 = Student(2,1,3)
        m4 = Student(6,1,3)
        g1 = Group(host1,2)
        g1.addMember(m1)
        g1.addMember(m4)

        host2 = Student(3,1,3)
        m2 = Student(4,1,3)
        m3 = Student(5,1,3)
        g2 = Group(host2,2)
        g2.addMember(m2)
        g2.addMember(m3)
        
        host3 = Student(7,1,3)
        formerGroup = Group(host3,1)
        for m in [m1,m2,m3,m4]:
            formerGroup.addMember(m)

        for m in [m1,m2,m3,m4]:
            m.assignGroup(formerGroup)
        
        groups = [self.group,g1,g2]

        self.assertFalse(self.move.performMove(self.group,groups))

    def test_CanSwapIf2FromDifferentGroupCanSwap(self):
        

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        m4 = Student(6,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        g1.addMember(m4)

        host2 = Student(3,0,3)
        m2 = Student(4,0,3)
        m3 = Student(5,0,3)
        g2 = Group(host2,1)
        g2.addMember(m2)
        g2.addMember(m3)
        
        groups = [self.group,g1,g2]

        self.assertTrue(self.move.performMove(self.group,groups))

        self.assertEqual(self.group.size,3)
        self.assertIn(m1,self.group.members)
        self.assertIn(m2,self.group.members)
        self.assertNotIn(m1,g1.members)
        self.assertNotIn(m2,g2.members)

    def test_CanSwapIf2FromSameGroupCanSwap(self):
        
        move = Swap2ToGroupMove(2,4)

        host1 = Student(1,0,3)
        m1 = Student(2,0,3)
        m3 = Student(6,0,3)
        m2 = Student(3,0,3)
        g1 = Group(host1,1)
        g1.addMember(m1)
        g1.addMember(m2)
        g1.addMember(m3)

        
        groups = [self.group,g1]

        self.assertTrue(move.performMove(self.group,groups))

        self.assertEqual(self.group.size,3)
        self.assertEqual(g1.size,2)
        self.assertIn(m1,self.group.members)
        self.assertIn(m2,self.group.members)
        self.assertNotIn(m1,g1.members)
        self.assertNotIn(m2,g1.members)
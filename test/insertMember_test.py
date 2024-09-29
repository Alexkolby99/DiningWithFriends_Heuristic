
import unittest
from src.student import Student
from src.group import Group
from src.constructionMoves import InsertMember

class TestinsertMember_move(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.move = InsertMember()
        self.student = Student(identifier=0,gender=1,num_groups=3)
  
    def testCannotInsertIfGroupedWithLast(self):
        host = Student(1,1,num_groups=3)
        formerGroup = Group(self.student,0)
        formerGroup.addMember(host)
        host.assignGroup(formerGroup)
        groups = [Group(host,1)]

        self.assertFalse(self.move.performMove(self.student,groups,1))


    def testCannotInsertIfGenderCountOfZero(self):
        host = Student(1,0,num_groups=3)
        groups = [Group(host,1)]

        self.assertFalse(self.move.performMove(self.student,groups,1))

    def testCannotBeGroupedWithIfAlreadyVisited(self):
        host = Student(1,1,num_groups=3)
        group = Group(host,0)
        group.addMember(self.student)
        self.student.assignGroup(group)
        host.assignGroup(group)
        groups = [Group(host,2)]

        self.assertFalse(self.move.performMove(self.student,groups,2))

    def testCanBeAddedElse(self):
        host = Student(1,1,num_groups=3)
        groups = [Group(host,1)]

        self.assertEqual(groups[0].members,[host])
        self.assertTrue(self.move.performMove(self.student,groups,1))
        self.assertEqual(groups[0].members,[host,self.student])


import unittest
from src.student import Student
from src.group import Group
from src.initializers import MaximizeDifferentHosts_initializer

class TestMaximizeDifferentHosts_initializer(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.t = 1
        self.initializer = MaximizeDifferentHosts_initializer()
        self.boys = [Student(identifier=1, gender=1,num_groups=1),
                Student(identifier=2, gender=1,num_groups=1),
                Student(identifier=3, gender=1,num_groups=1),
                Student(identifier=0, gender=1,num_groups=1)]# Add some members for testing

        self.girls = [Student(identifier=4, gender=0,num_groups=1),
                Student(identifier=5, gender=0,num_groups=1),
                Student(identifier=6, gender=0,num_groups=1),
                Student(identifier=7, gender=0,num_groups=1)]

        self.boys[0].addHostTime()
        self.boys[1].addHostTime()
        self.girls[0].addHostTime()
        self.girls[1].addHostTime()
        

    def test4GroupsAreMade(self):

        groups,_ = self.initializer.initializeGroups(self.boys,self.girls,4,4,self.t)

        self.assertEqual(len(groups),4)

    def testHostHasZeroHostTimes(self):

        groups,_ = self.initializer.initializeGroups(self.boys,self.girls,4,4,self.t)
        for group in groups:
            self.assertEqual(group.host.hostTimes,0)

    def testHostHasOneHostTimes(self):
        self.boys[0].addHostTime()
        self.boys[2].addHostTime()
        groups,_ = self.initializer.initializeGroups(self.boys,self.girls,4,4,self.t)
        for group in groups:
            self.assertNotEqual(group.host.hostTimes,2)

    def testReturnsErrorIfNotEnoughStudents(self):

        self.boys.pop()

        with self.assertRaises(AssertionError):
            self.initializer.initializeGroups(self.boys,self.girls,4,4,self.t)
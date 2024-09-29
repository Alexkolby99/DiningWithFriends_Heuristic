import unittest

import numpy.testing as npt
import numpy as np
from src import student


class TestStudent(unittest.TestCase):

    def setUp(self) -> None:
        self.testObject = student(2,1,2,2)

    def test_numberWorks(self):
        self.assertEqual(self.testObject.number,1)

    def test_typeWorks(self):
        self.assertEqual(self.testObject.type,2)

    def test_hostTimesProperty(self):
        self.assertEqual(self.testObject.hostTimes,0)

    def test_hostEvents(self):
        self.assertEqual(self.testObject.hostEvents,[False,False])

    def test_setHostTime(self):
        self.testObject.setHostTime(0)
        self.assertEqual(self.testObject.hostEvents,[True,False])
    
    def test_setHostTimeTwice(self):
        self.testObject.setHostTime(1)
        self.testObject.setHostTime(0)
        self.assertEqual(self.testObject.hostEvents,[True,True])

    def test_hostTimesIncrease(self):
        self.testObject.setHostTime(1)
        self.assertEqual(self.testObject.hostTimes,1)

    def test_removeHostTime(self):
        self.testObject.setHostTime(1)
        self.testObject.removeHostTime(1)
        self.assertEqual(self.testObject.hostTimes,0)

    def test_hostTimeRemoveOnlyIfActuallyRemoves(self):
        self.testObject.removeHostTime(1)
        self.assertEqual(self.testObject.hostTimes,0)

    def test_hostTimeAddOnlyIfActuallyAdd(self):
        self.testObject.setHostTime(1)
        self.testObject.setHostTime(1)
        self.assertEqual(self.testObject.hostTimes,1)

    def test_setGrouptime0(self):
        self.testObject.setGroup('group',0)
        self.assertEqual(self.testObject.group,['group',None])


    def test_setGrouptime1(self):
        self.testObject.setGroup('group',1)
        self.assertEqual(self.testObject.group,[None,'group'])

    
    def test_setGrouptime0and1(self):
        self.testObject.setGroup('group1',1)
        self.testObject.setGroup('group0',0)
        self.assertEqual(self.testObject.group,['group0','group1'])


    def test_groupingOptions(self):      
        npt.assert_array_equal(self.testObject.groupingOptions,np.array([[True,False],
                                                          [True,False]]))
        
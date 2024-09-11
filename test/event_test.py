import unittest
from src import event


class TestEvent(unittest.TestCase):

    def setUp(self) -> None:
        self.testObject = event()

    def test_TimeStampNonePerDefault(self):
        self.assertIsNone(self.testObject.timestamp)

    def test_TimeStampProperty(self):
        self.testObject.timestamp = 1
        self.assertEqual(self.testObject.timestamp,1)
    
    def test_groupsIsEmptyListPerDefault(self):
        self.assertEqual(self.testObject.groups,[])

    def test_groupsProperty(self):
        self.testObject.groups = [1,2]
        self.assertEqual(self.testObject.groups,[1,2])

    def test_AddGroup(self):
        self.testObject.addGroup(1)
        self.assertIn(1,self.testObject.groups)

    def test_deleteFromGroup(self):
        self.testObject.addGroup(1)
        self.testObject.addGroup(2)
        self.testObject.removeGroup(1)
        self.assertIn(2,self.testObject.groups)
        self.assertNotIn(1,self.testObject.groups)
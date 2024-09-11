import unittest
from src import group


class TestGroup(unittest.TestCase):

    def setUp(self) -> None:
        self.testObject = group()

    def test_hostProperty(self):
        self.testObject.host = 'myHost'
        self.assertEqual(self.testObject.host,'myHost')

    def test_memberProperty(self):
        self.testObject.members = ['1','2']
        self.assertEqual(self.testObject.members,['1','2'])

    def test_AddMemberAddsToMemberList(self):
        self.testObject.addMember('x')
        self.assertEqual(self.testObject.members,['x'])

    def test_AddMemberIfAlreadyOneMember(self):
        self.testObject.addMember('x')
        self.testObject.addMember('y')
        self.assertIn('x',self.testObject.members)
        self.assertIn('y',self.testObject.members)

    def test_RemoveMember(self):
        self.testObject.addMember('x')
        self.testObject.addMember('y')
        self.testObject.removeMember('x')
        self.assertNotIn('x',self.testObject.members)
        self.assertIn('y',self.testObject.members)
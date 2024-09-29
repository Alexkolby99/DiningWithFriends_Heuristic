import unittest

from src.group import Group
from src.student import Student

# Assuming Student and Group classes are defined elsewhere and imported
class TestGroup(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.host_student = Student(identifier=1, gender=1,num_groups=1)
        self.group = Group(host=self.host_student, timestamp=1234567890)
        
        # Add some members for testing
        self.student1 = Student(identifier=2, gender=0,num_groups=1)
        self.student2 = Student(identifier=3, gender=1,num_groups=1)
        self.group.addMember(self.student1)
        self.group.addMember(self.student2)

    def test_initialization(self):
        '''Test that the group is initialized correctly'''
        self.assertEqual(self.group.host, self.host_student)
        self.assertEqual(self.group.size, 3)
        self.assertEqual(self.group.t, 1234567890)
        self.assertIn(self.student1, self.group.members)
        self.assertIn(self.student2, self.group.members)

    def test_add_member(self):
        '''Test adding a member to the group'''
        new_student = Student(identifier=4, gender=0,num_groups=1)
        self.group.addMember(new_student)
        self.assertIn(new_student, self.group.members)
        self.assertEqual(self.group.size, 4)

    def test_add_duplicate_member(self):
        '''Test adding a duplicate member to the group'''
        self.group.addMember(self.student1)  # Adding student1 again
        self.assertEqual(self.group.size, 3)  # Size should remain the same
        self.assertEqual(len(self.group.members), 3)  # No duplicates in members

    def test_remove_member(self):
        '''Test removing a member from the group'''
        self.group.removeMember(self.student1)
        self.assertNotIn(self.student1, self.group.members)
        self.assertEqual(self.group.size, 2)

    def test_remove_non_member(self):
        '''Test removing a non-member from the group'''
        non_member = Student(identifier=5, gender=1,num_groups=1)
        self.group.removeMember(non_member)  # Should do nothing, no error
        self.assertEqual(self.group.size, 3)  # Size should remain unchanged

    def test_host_property(self):
        '''Test that the host property returns the correct value'''
        self.assertEqual(self.group.host, self.host_student)

    def test_members_property(self):
        '''Test that the members property returns the correct members'''
        self.assertEqual(self.group.members, [self.host_student,self.student1, self.student2])

    def test_group_timestamp(self):
        '''Test that the timestamp property returns the correct value'''
        self.assertEqual(self.group.t, 1234567890)

    def testGenderCount(self):
        self.assertEqual(self.group.getGenderCount(0),1)
        self.assertEqual(self.group.getGenderCount(1),2)

    def testRemovingReducesGenderCount(self):
        self.group.removeMember(self.student1)
        self.assertEqual(self.group.getGenderCount(0),0)
        self.assertEqual(self.group.getGenderCount(1),2)
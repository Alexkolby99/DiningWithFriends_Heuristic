import unittest
from src.group import Group
from src.student import Student
from src.event import Event

class TestEvent(unittest.TestCase):
    def setUp(self):
        '''Set up test cases'''
        self.host1 = Student(identifier=1, gender=1,num_groups=1)
        self.host2 = Student(identifier=2, gender=0,num_groups=1)
        self.group1 = Group(host=self.host1, timestamp=1234567890)
        self.group2 = Group(host=self.host2, timestamp=1234567891)
        self.event = Event(timestamp=1234567892)

        # Add initial hosts and groups
        self.event.addHost(self.host1)
        self.event.addGroup(self.group1)

    def test_initialization(self):
        '''Test that the event is initialized correctly'''
        self.assertEqual(self.event.timeStamp, 1234567892)
        self.assertEqual(len(self.event.hosts), 1)
        self.assertIn(self.host1, self.event.hosts)
        self.assertEqual(len(self.event.groups), 1)
        self.assertIn(self.group1, self.event.groups)

    def test_add_group(self):
        '''Test adding a group to the event'''
        self.event.addGroup(self.group2)
        self.assertIn(self.group2, self.event.groups)
        self.assertEqual(len(self.event.groups), 2)

    def test_add_duplicate_group(self):
        '''Test adding a duplicate group to the event'''
        self.event.addGroup(self.group1)  # Adding group1 again
        self.assertEqual(len(self.event.groups), 1)  # Size should remain the same

    def test_remove_group(self):
        '''Test removing a group from the event'''
        self.event.removeGroup(self.group1)
        self.assertNotIn(self.group1, self.event.groups)
        self.assertEqual(len(self.event.groups), 0)

    def test_remove_non_member_group(self):
        '''Test removing a group that is not in the event'''
        self.event.removeGroup(self.group2)  # Should do nothing, no error
        self.assertEqual(len(self.event.groups), 1)  # Size should remain unchanged

    def test_add_host(self):
        '''Test adding a host to the event'''
        self.event.addHost(self.host2)
        self.assertIn(self.host2, self.event.hosts)
        self.assertEqual(len(self.event.hosts), 2)

    def test_add_duplicate_host(self):
        '''Test adding a duplicate host to the event'''
        self.event.addHost(self.host1)  # Adding host1 again
        self.assertEqual(len(self.event.hosts), 1)  # Size should remain the same

    def test_remove_host(self):
        '''Test removing a host from the event'''
        self.event.removeHost(self.host1)
        self.assertNotIn(self.host1, self.event.hosts)
        self.assertEqual(len(self.event.hosts), 0)

    def test_remove_non_member_host(self):
        '''Test removing a host that is not in the event'''
        self.event.removeHost(self.host2)  # Should do nothing, no error
        self.assertEqual(len(self.event.hosts), 1)  # Size should remain unchanged

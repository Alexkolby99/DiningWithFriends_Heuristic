import unittest
from src.student import Student

class ExampleGroup():
    def __init__(self, name: str):
        self._name = name

    @property
    def group_name(self) -> str:
        return self._name


class TestStudent(unittest.TestCase):
    
    def setUp(self):
        '''Set up test cases'''
        self.student = Student(identifier=1, gender=1, num_groups=5)

    def test_initialization(self):
        '''Test that the student is initialized correctly'''
        self.assertEqual(self.student.identifier, 1)
        self.assertEqual(self.student.gender, 1)
        self.assertEqual(self.student.hostTimes, 0)
        self.assertEqual(len(self.student.groups), 5)

    def test_add_host_time(self):
        '''Test adding host times'''
        self.student.addHostTime()
        self.assertEqual(self.student.hostTimes, 1)

    def test_remove_host_time(self):
        '''Test removing host times'''
        self.student.addHostTime()  # Increment once
        self.student.removeHostTime()  # Should decrement
        self.assertEqual(self.student.hostTimes, 0)
        
        # Testing that it doesn't go below zero
        self.student.removeHostTime()
        self.assertEqual(self.student.hostTimes, 0)

    def test_add_student_that_visited(self):
        '''Test adding students that visited'''
        visitor = Student(identifier=2, gender=0, num_groups=3)
        self.student.addStudentThatVisited(visitor)
        self.assertIn(visitor, self.student.studentsThatVisited)

    def test_multiple_host_times(self):
        '''Test adding and removing multiple host times'''
        for _ in range(3):
            self.student.addHostTime()
        self.assertEqual(self.student.hostTimes, 3)
        
        for _ in range(2):
            self.student.removeHostTime()
        self.assertEqual(self.student.hostTimes, 1)

    def test_visited_students(self):
        '''Test that the visited students list is correctly maintained'''
        visitor1 = Student(identifier=2, gender=1, num_groups=2)
        visitor2 = Student(identifier=3, gender=0, num_groups=2)
        
        self.student.addStudentThatVisited(visitor1)
        self.student.addStudentThatVisited(visitor2)

        self.assertIn(visitor1, self.student.studentsThatVisited)
        self.assertIn(visitor2, self.student.studentsThatVisited)
        self.assertEqual(len(self.student.studentsThatVisited), 2)
        
import unittest



class TestStudent(unittest.TestCase):

    def setUp(self) -> None:
        self.testObject = None

    def test_1(self):
        self.testObject
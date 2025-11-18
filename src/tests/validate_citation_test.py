import unittest
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_length_does_not_raise_error(self):
        validate_citation("Electronic Commerce", "Michael Merz", "1999")


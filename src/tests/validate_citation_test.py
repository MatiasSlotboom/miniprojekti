import unittest
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_length_does_not_raise_error(self):
        validate_citation("Electronic Commerce", "Michael Merz", "1999", "book")
    
    def test_empty_title_raises_error(self):
        self.assertRaises(UserInputError, validate_citation, "", "Author", "2015", "book")
    
    def test_negative_date_raises_error(self):
        self.assertRaises(UserInputError, validate_citation, "Title", "Author", "-1", "book")
    
    def test_non_valid_type_raises_error(self):
        self.assertRaises(UserInputError, validate_citation, "Title", "Author", "2015", "magazine")
    
    def test_date_not_number_raises_error(self):
        self.assertRaises(UserInputError, validate_citation, "Title", "Author", "another author", "bible")


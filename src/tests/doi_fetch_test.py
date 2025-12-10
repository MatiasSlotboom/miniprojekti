import unittest
import requests
from unittest.mock import patch, Mock
from util import fetch_doi_metadata, DOIError

class TestDOIFetch(unittest.TestCase):
    
    @patch('util.requests.get')
    def test_fetch_doi_metadata_success(self, mock_get):
        """Test successful DOI metadata fetch"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': {
                'title': ['Test Article Title'],
                'author': [
                    {'given': 'John', 'family': 'Doe'}
                ],
                'published-print': {
                    'date-parts': [[2020, 1, 1]]
                }
            }
        }
        mock_get.return_value = mock_response
        
        result = fetch_doi_metadata('10.1234/test.doi')
        
        self.assertEqual(result['title'], 'Test Article Title')
        self.assertEqual(result['author'], 'John Doe')
        self.assertEqual(result['year'], '2020')
    
    @patch('util.requests.get')
    def test_fetch_doi_metadata_404(self, mock_get):
        """Test DOI not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(DOIError) as context:
            fetch_doi_metadata('10.1234/invalid.doi')
        
        self.assertIn('not found', str(context.exception))
    
    @patch('util.requests.get')
    def test_fetch_doi_metadata_timeout(self, mock_get):
        """Test request timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with self.assertRaises(DOIError) as context:
            fetch_doi_metadata('10.1234/test.doi')
        
        self.assertIn('timed out', str(context.exception))
    
    def test_fetch_doi_empty_string(self):
        """Test empty DOI string"""
        with self.assertRaises(DOIError) as context:
            fetch_doi_metadata('')
        
        self.assertIn('cannot be empty', str(context.exception))
    
    @patch('util.requests.get')
    def test_fetch_doi_with_prefix(self, mock_get):
        """Test DOI with various prefixes"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': {
                'title': ['Test Title'],
                'author': [{'given': 'Jane', 'family': 'Smith'}],
                'published-print': {'date-parts': [[2021]]}
            }
        }
        mock_get.return_value = mock_response
        
        # Test with doi: prefix
        result = fetch_doi_metadata('doi:10.1234/test')
        self.assertIsNotNone(result)
        
        # Test with https://doi.org/ prefix
        result = fetch_doi_metadata('https://doi.org/10.1234/test')
        self.assertIsNotNone(result)

import unittest
from unittest.mock import patch, MagicMock
from app import app, titlefixer, bibselector, bibcontent

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
    
    def test_titlefixer(self):
        self.assertEqual(titlefixer("Hello World!"), "Hello_World")
        self.assertEqual(titlefixer("Multiple   Spaces"), "Multiple_Spaces")
        self.assertEqual(titlefixer("Special@Chars#"), "SpecialChars")
    
    @patch("app.get_citations")
    def test_bibselector_get_citations_called(self, mock_get_citations):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        citation_mock.type = "misc"
        mock_get_citations.return_value = [citation_mock]

        result = bibselector()
        self.assertEqual(len(result), 1)
        self.assertIn("Test Title", result[0]["text"])
        mock_get_citations.assert_called_once()
    
    @patch("app.get_citations")
    def test_bibcontent_bibselector_called(self, mock_get_citations):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        citation_mock.type = "misc"
        mock_get_citations.return_value = [citation_mock]

        content = bibcontent()
        self.assertIn("Test", content)
    
    @patch("app.get_citations")
    def test_index_route(self, mock_get_citations):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        mock_get_citations.return_value = [citation_mock]
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        mock_get_citations.assert_called_once()
    
    @patch("app.get_citations")
    def test_index(self, mock_get_citations):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        mock_get_citations.return_value = [citation_mock]
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        mock_get_citations.assert_called_once()
    
    def test_new_citation_route(self):
        response = self.client.get("/new_citation")
        self.assertEqual(response.status_code, 200)
    
    @patch("app.create_citation")
    @patch("app.validate_citation")
    def test_create_citation(self, mock_validate, mock_create):
        data = {
            "title": "Test Title",
            "author": "Test Author",
            "date": "2015",
            "type": "misc"
        }
        response = self.client.post("/create_citation", data=data, follow_redirects=True)
        mock_validate.assert_called_once_with("Test Title", "Test Author", "2015", "misc")
        mock_create.assert_called_once_with("Test Title", "Test Author", "2015", "misc", 
                                            journal=None, booktitle=None, publisher=None, 
                                            volume=None, number=None, pages=None, editor=None, 
                                            edition=None, institution=None, note=None)
        self.assertEqual(response.status_code, 200)
    
    @patch("app.validate_citation")
    @patch("app.create_citation")
    def test_create_citation_exception(self, mock_create, mock_validate):
        mock_validate.return_value = None
        mock_create.side_effect = Exception("DB error")
        data = {
            "title": "Test Title",
            "author": "Test Author",
            "date": "2015",
            "type": "misc"
        }
        response = self.client.post("/create_citation", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    
    @patch("app.delete_citation")
    def test_remove_citation_route(self, mock_delete):
        response = self.client.post("/remove_citation/1", follow_redirects=True)
        mock_delete.assert_called_once_with(1)
        self.assertEqual(response.status_code, 200)
    
    @patch("app.bibcontent")
    def test_download_bib(self, mock_bibcontent):
        mock_bibcontent.return_value = "@misc{test, title={Test Title}, author={Test Author}, year={2015}}"
        response = self.client.get("/download_bib")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"@misc{test", response.data)
    
    @patch("app.bibselector")
    def test_download_selected(self, mock_bibselector):
        mock_entry = {"id": "1", "text": "@misc{test, title={Test Title}}", "title": "Test Title", "author": "Test Author", "date": "2015"}
        mock_bibselector.return_value = [mock_entry]
        response = self.client.post("/download_selected", data={"selected": ["1"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"@misc{test", response.data)
    
    @patch("app.get_citation")
    def test_show_citation_route(self, mock_get_citation):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        mock_get_citation.return_value = citation_mock

        response = self.client.get("/show_citation/1")
        self.assertEqual(response.status_code, 200)
    
    @patch("app.get_citation")
    @patch("app.update_citation")
    @patch("app.validate_citation")
    def test_edit_citation_post(self, mock_validate, mock_update, mock_get_citation):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Test Title"
        citation_mock.author = "Test Author"
        citation_mock.date = 2015
        citation_mock.type = "misc"
        mock_get_citation.return_value = citation_mock
        data = {
            "title": "New Test Title",
            "author": "New Test Author",
            "date": "2016",
            "type": "misc"
        }
        response = self.client.post("/edit_citation/1", data=data, follow_redirects=True)
        mock_validate.assert_called_once_with("New Test Title", "New Test Author", "2016", "misc")
        mock_update.assert_called_once_with(1, "New Test Title", "New Test Author", "2016", "misc",
                                            journal=None, booktitle=None, publisher=None,
                                            volume=None, number=None, pages=None, editor=None,
                                            edition=None, institution=None, note=None)
        self.assertEqual(response.status_code, 200)
    
    @patch("app.get_citation")
    @patch("app.update_citation")
    @patch("app.validate_citation")
    def test_edit_citation_exception(self, mock_validate, mock_update, mock_get_citation):
        citation_mock = MagicMock()
        citation_mock.id = 1
        citation_mock.title = "Old Title"
        citation_mock.author = "Author"
        citation_mock.date = 2025
        citation_mock.type = "misc"
        mock_get_citation.return_value = citation_mock
        mock_validate.return_value = None
        mock_update.side_effect = Exception("DB error")
        data = {
            "title": "New Test Title",
            "author": "New Test Author",
            "date": "2016",
            "type": "misc"
        }
        response = self.client.post("/edit_citation/1", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    




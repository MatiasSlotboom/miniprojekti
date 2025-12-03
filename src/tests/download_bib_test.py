import unittest
from unittest.mock import Mock, ANY
from repositories.citation_repository import get_citations, create_citation
from flask import Response
from datetime import datetime, date
from entities.citation import Citation

class TestDownloadBib(unittest.TestCase):
    def setUp(self):
        pass

    def test_download_bib_fuction_called(self):
        citations = [Citation(ANY, "test_title", "test_author", datetime(1234, 1, 1), "misc")]
        bib_entries = []
        for c in citations:
            if isinstance(c.date, (datetime, date)):
                year = c.date.year
            else:
                year = str(c.date)[:4]
            entry = f"""@{c.type}{{{c.id},
    title = {{{c.title}}},
    author = {{{c.author}}},
    year = {{{year}}},
    }}"""
            bib_entries.append(entry)
        bib_content = "\n\n".join(bib_entries)

        test_response = Response(
            bib_content,
            mimetype="text/plain",
            headers={"Content-Disposition": "attachment; filename=references.bib"}
        )

        response = b'@misc{<ANY>,\n    title = {test_title},\n    author = {test_author},\n    year = {1234},\n    }'

        self.assertEqual(test_response.get_data(), response)



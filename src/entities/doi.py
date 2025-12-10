class DOI:  # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    def __init__(self, doi_id, title=None, author=None, date=None, citation_type=None,
                 journal=None, booktitle=None, publisher=None, volume=None,
                 number=None, pages=None, editor=None, edition=None,
                 institution=None, note=None):
        self.id = doi_id
        self.title = title
        self.author = author
        self.date = date
        self.type = citation_type
        self.journal = journal
        self.booktitle = booktitle
        self.publisher = publisher
        self.volume = volume
        self.number = number
        self.pages = pages
        self.editor = editor
        self.edition = edition
        self.institution = institution
        self.note = note

    def __str__(self):
        return f"""{self.title} by {self.author}, dated {self.date} {self.type} in {self.journal}{self.booktitle}{self.publisher}
                    {self.volume}{self.number}{self.pages}{self.editor}{self.edition}{self.institution}{self.note}"""

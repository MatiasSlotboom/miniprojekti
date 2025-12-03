class Citation:
    def __init__(self, citation_id, title, author, date, citation_type):
        self.id = citation_id
        self.title = title
        self.author = author
        self.date = date.year
        self.type = citation_type

    def __str__(self):
        return f"{self.title} by {self.author}, dated {self.date} {self.type}"

class Citation:
    def __init__(self, citation_id, title, author, date):
        self.id = citation_id
        self.title = title
        self.author = author
        self.date = date.year

    def __str__(self):
        return f"{self.title} by {self.author}, dated {self.date}"

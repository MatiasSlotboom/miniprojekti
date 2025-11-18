class Citation:
    def __init__(self, id, title, author, date):
        self.id = id
        self.title = title
        self.author = author
        self.date = date

    def __str__(self):
        return f"{self.title} by {self.author}, dated {self.date}"
class UserInputError(Exception):
    pass

def validate_citation(title, author, date):
    if len(title) == 0 or len(author) == 0 or len(date) == 0:
        raise UserInputError("Citation fields cannot be empty")
class UserInputError(Exception):
    pass

def validate_citation(title, author, date):
    if len(title) == 0 or len(author) == 0 or len(date) == 0:
        raise UserInputError("Citation fields cannot be empty")
    try:
        if int(date) < 0:
            raise UserInputError("Date must be a positive number")
    except ValueError:
        raise UserInputError("Date must be a number")

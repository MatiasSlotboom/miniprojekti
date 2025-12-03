valid_citation_types = ['article', 'book', 'misc']

class UserInputError(Exception):
    pass

def validate_citation(title, author, date, citation_type):
    if len(title) == 0 or len(author) == 0 or len(date) == 0:
        raise UserInputError("Citation fields cannot be empty")
    try:
        if int(date) < 0:
            raise UserInputError("Date must be a positive number")
    except ValueError as error:
        raise UserInputError("Date must be a number") from error
    if citation_type not in valid_citation_types:
        raise UserInputError(f"Invalid citation type. Must be one of: {', '.join(valid_citation_types)}")

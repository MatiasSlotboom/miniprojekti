import requests

valid_citation_types = ['article', 'book', 'misc']

class UserInputError(Exception):
    pass

class DOIError(Exception):
    pass
# pylint: disable=unused-argument
def validate_citation(title, author, date, citation_type, journal=None, booktitle=None, publisher=None,
                      volume=None, number=None, pages=None, editor=None, edition=None, institution=None, note=None):
    if len(title) == 0 or len(author) == 0 or len(date) == 0:
        raise UserInputError("Citation fields cannot be empty")
    try:
        if int(date) < 0:
            raise UserInputError("Date must be a positive number")
    except ValueError as error:
        raise UserInputError("Date must be a number") from error
    if citation_type not in valid_citation_types:
        raise UserInputError(f"Invalid citation type. Must be one of: {', '.join(valid_citation_types)}")

def fetch_doi_metadata(doi):  # pylint: disable=too-many-branches
    if not doi or doi.strip() == '':
        raise DOIError("DOI cannot be empty")

    doi = doi.strip()
    if doi.startswith('doi:'):
        doi = doi[4:]
    elif doi.startswith('https://doi.org/'):
        doi = doi[16:]
    elif doi.startswith('http://doi.org/'):
        doi = doi[15:]

    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            raise DOIError("DOI not found")

        response.raise_for_status()
        data = response.json()

        message = data.get('message', {})

        title = ', '.join(message.get('title', []))

        authors = message.get('author', [])
        author = ', '.join([f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors])

        year = None
        if 'published-print' in message and 'date-parts' in message['published-print']:
            date_parts = message['published-print']['date-parts']
            if date_parts and len(date_parts) > 0 and len(date_parts[0]) > 0:
                year = str(date_parts[0][0])
        elif 'published-online' in message and 'date-parts' in message['published-online']:
            date_parts = message['published-online']['date-parts']
            if date_parts and len(date_parts) > 0 and len(date_parts[0]) > 0:
                year = str(date_parts[0][0])
        elif 'indexed' in message and 'date-parts' in message['indexed']:
            date_parts = message['indexed']['date-parts']
            if date_parts and len(date_parts) > 0 and len(date_parts[0]) > 0:
                year = str(date_parts[0][0])

        return {
            'title': title,
            'author': author,
            'year': year or '',
            'raw_data': message
        }

    except requests.exceptions.Timeout as error:
        raise DOIError("Request timed out") from error
    except requests.exceptions.RequestException as error:
        raise DOIError(f"Failed to fetch DOI metadata: {str(error)}") from error

def validate_doi(doi):
    try:
        return fetch_doi_metadata(doi)
    except DOIError as error:
        raise UserInputError(f"Invalid DOI: {str(error)}") from error

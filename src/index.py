from app import app
import json
from crossref import CrossRefAPIClient

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)

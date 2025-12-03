from flask import redirect, render_template, request, jsonify, flash, Response
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation, delete_citation, get_citation
from config import app, test_env
from util import validate_citation

def bibcontent():
    citations = get_citations()
    bib_entries = []
    for c in citations:

        entry = (
            f"@misc{{{c.id},\n"
            f"  title = {{{c.title}}},\n"
            f"  author = {{{c.author}}},\n"
            f"  year = {{{str(c.date)}}},\n"
            f"}}"
        )

        bib_entries.append(entry)

    return "\n\n".join(bib_entries)

@app.route("/")
def index():
    citations = get_citations()
    unfinished = len(list(citations))
    return render_template("index.html", citations=citations, unfinished=unfinished)

@app.route("/new_citation")
def new():
    return render_template("new_citation.html")

@app.route("/create_citation", methods=["POST"])
def todo_creation():
    title = request.form.get("title")
    author = request.form.get("author")
    date = request.form.get("date")
    print(f"Received citation: {title}, {author}, {date}")

    try:
        validate_citation(title, author, date)
        print(f"In the middle of citation: {title}, {author}, {date}")
        create_citation(title, author, date)
        print(f"Created citation: {title}, {author}, {date}")
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_citation")

@app.route("/remove_citation/<int:citation_id>", methods=["POST"])
def remove_citation(citation_id):
    delete_citation(citation_id)
    return redirect("/")

@app.route("/download_bib")
def download_bib():
    return Response(
        bibcontent(),
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=references.bib"}
    )
@app.route("/copy_bib")
def copy_bib():
    return Response(
        bibcontent(),
        mimetype="text/plain",
    )

@app.route("/show_citation/<int:citation_id>")
def show_citation(citation_id):
    citation = get_citation(citation_id)
    return render_template("show_citation.html", citation=citation)

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

    @app.route("/create_test_citation")
    def create_test_citation():
        create_citation("Testilähde", "Testitekijä", "1900")
        return redirect("/")

    @app.route("/create_two_test_citations")
    def create_two_test_citations():
        create_citation("Testilähde1", "Testitekijä1", "1901")
        create_citation("Testilähde2", "Testitekijä2", "1902")
        return redirect("/")

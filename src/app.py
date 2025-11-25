from datetime import datetime, date
from flask import redirect, render_template, request, jsonify, flash, Response
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation
from config import app, test_env
from util import validate_citation

@app.route("/")
def index():
    citations = get_citations()
    unfinished = len([citation for citation in citations])
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

@app.route("/download_bib")
def download_bib():
    citations = get_citations()
    bib_entries = []
    for c in citations:
        if isinstance(c.date, (datetime, date)):
            year = c.date.year
        else:
            year = str(c.date)[:4]
        entry = f"""@misc{{{c.id},
            title = {{{c.title}}},
            author = {{{c.author}}},
            year = {{{year}}},
            }}"""
        bib_entries.append(entry)
    bib_content = "\n\n".join(bib_entries)

    return Response(
        bib_content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=references.bib"}
    )

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

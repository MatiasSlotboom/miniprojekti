from flask import redirect, render_template, request, jsonify, flash
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

    try:
        validate_citation(title, author, date)
        create_citation(title, author, date)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_citation")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

import re
import json
from flask import redirect, render_template, request, jsonify, flash, Response
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation, delete_citation, get_citation, update_citation, get_doi
from config import app, test_env
from util import validate_citation, valid_citation_types, validate_doi

def titlefixer(title):
    title = re.sub(r'\s+', '_', title)
    title = re.sub(r'[^0-9a-zA-Z_]', '', title)
    return title

def bibselector():
    citations = get_citations()
    bib_entries = []

    for c in citations:
        safe_title = titlefixer(c.title)
        key = f"{safe_title}-{c.date}-{c.id}"

        entry = (
            f"@misc{{{key},\n"
            f"  title = {{{c.title}}},\n"
            f"  author = {{{c.author}}},\n"
            f"  year = {{{str(c.date)}}},\n"
            f"}}"
        )

        bib_entries.append({
            "id": str(c.id),
            "text": entry,
            "title": c.title,
            "author": c.author,
            "date": str(c.date)
        })

    return bib_entries

def bibcontent():
    entries = bibselector()
    return "\n\n".join(e["text"] for e in entries)

@app.route("/")
def index():
    citations = get_citations()
    unfinished = len(list(citations))
    return render_template("index.html", citations=citations, unfinished=unfinished)

@app.route("/new_citation")
def new():
    return render_template("new_citation.html", citation_types=valid_citation_types)

@app.route("/fill_with_doi", methods=["POST"])
def fill_with_doi():
    doi_address = request.form.get("doi")
    print(doi_address)

    try:
        work = validate_doi(doi_address)
        print("validoitu !!")
        print(get_doi(work.json()))
        return redirect("/new_citation")

    except Exception as error:
        flash(str(error))
        return redirect("/new_citation")

@app.route("/create_citation", methods=["POST"])
def todo_creation():
    title = request.form.get("title")
    author = request.form.get("author")
    date = request.form.get("date")
    citation_type = request.form.get("type", "misc")
    journal = request.form.get("journal")
    booktitle = request.form.get("booktitle")
    publisher = request.form.get("publisher")
    volume = request.form.get("volume")
    number = request.form.get("number")
    pages = request.form.get("pages")
    editor = request.form.get("editor")
    edition = request.form.get("edition")
    institution = request.form.get("institution")
    note = request.form.get("note")
    print(f"""Received citation: {title}, {author}, {date}, {citation_type}, {journal}, {booktitle}, {publisher},
           {volume}, {number}, {pages}, {editor}, {edition}, {institution}, {note}""")

    try:
        validate_citation(title, author, date, citation_type)
        print(f"""In the middle of citation: {title}, {author}, {date}, {citation_type}, {journal}, {booktitle}, {publisher},
              {volume}, {number}, {pages}, {editor}, {edition}, {institution}, {note}""")
        create_citation(title, author, date, citation_type,
                    journal=journal, booktitle=booktitle, publisher=publisher, volume=volume,
                    number=number, pages=pages, editor=editor, edition=edition,
                    institution=institution, note=note)
        print(f"""Created citation: {title}, {author}, {date}, {citation_type}, {journal}, {booktitle}, {publisher},
               {volume}, {number}, {pages}, {editor}, {edition}, {institution}, {note}""")
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

@app.route("/downloads")
def downloads():
    entries = bibselector()
    return render_template("downloads.html", entries=entries)

@app.route("/download_selected", methods=["POST"])
def download_selected():
    selected = request.form.getlist("selected")
    selected_ids = []
    for item in selected:
        selected_ids.extend(v.strip() for v in item.split(",") if v.strip())
    entries = bibselector()
    selected_entries = [e["text"] for e in entries if e["id"] in selected_ids]
    output = "\n\n".join(selected_entries)

    return Response(
        output,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=references.bib"}
    )

@app.route("/copy_bib")
def copy_bib():
    return Response(
        bibcontent(),
        mimetype="text/plain",
    )

@app.route("/copy_selected", methods=["POST"])
def copy_selected():
    selected = request.form.getlist("selected")
    selected_ids = []
    for item in selected:
        selected_ids.extend(v.strip() for v in item.split(",") if v.strip())
    entries = bibselector()
    selected_entries = [e["text"] for e in entries if e["id"] in selected_ids]
    output = "\n\n".join(selected_entries)
    return Response(output, mimetype="text/plain")

@app.route("/show_citation/<int:citation_id>")
def show_citation(citation_id):
    citation = get_citation(citation_id)
    print("got citation:", citation, "for id:", citation_id)
    return render_template("show_citation.html", citation=citation)

@app.route("/edit_citation/<int:citation_id>", methods=["get", "post"])
def edit_citation(citation_id):
    citation = get_citation(citation_id)

    if request.method == "GET":
        print("got citation:", citation, "for id:", citation_id)
        return render_template("edit_citation.html", citation=citation, citation_types = valid_citation_types)

    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        date = request.form.get("date")
        citation_type = request.form.get("type", "misc")
        journal = request.form.get("journal")
        booktitle = request.form.get("booktitle")
        publisher = request.form.get("publisher")
        volume = request.form.get("volume")
        number = request.form.get("number")
        pages = request.form.get("pages")
        editor = request.form.get("editor")
        edition = request.form.get("edition")
        institution = request.form.get("institution")
        note = request.form.get("note")
        print(f"""Received citation: {title}, {author}, {date}, {citation_type}, {journal}, {booktitle}, {publisher},
               {volume}, {number}, {pages}, {editor}, {edition}, {institution}, {note}""")

        try:
            validate_citation(title, author, date, citation_type)
            update_citation(citation_id, title, author, date, citation_type, journal=journal,
                    booktitle=booktitle, publisher=publisher, volume=volume,
                    number=number, pages=pages, editor=editor, edition=edition,
                    institution=institution, note=note)
            return redirect("/")
        except Exception as error:
            flash(str(error))
            return redirect("/edit_citation/" + str(citation_id))
    return redirect("/")

@app.route("/copy_bib_citation/<int:citation_id>")
def copy_bib_citation(citation_id):
    c = get_citation(citation_id)
    safe_title = titlefixer(c.title)
    key = f"{safe_title}-{c.date}-{c.id}"

    entry = (
        f"@{c.type}{{{key},\n"
        f"  title = {{{c.title}}},\n"
        f"  author = {{{c.author}}},\n"
        f"  year = {{{str(c.date)}}},\n"
        f"}}"
    )

    return Response(
        entry,
        mimetype="text/plain"
    )

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

    @app.route("/create_test_citation")
    def create_test_citation():
        create_citation("Testilähde", "Testitekijä", "1900", "misc")
        return redirect("/")

    @app.route("/create_two_test_citations")
    def create_two_test_citations():
        create_citation("Testilähde1", "Testitekijä1", "1901", "misc")
        create_citation("Testilähde2", "Testitekijä2", "1902", "misc")
        return redirect("/")

    @app.route("/create_thirty_test_citations")
    def create_thirty_test_citations():
        titles = [
            "Machine Learning Fundamentals", "Web Development Guide", "Data Science Basics",
            "Python Programming", "JavaScript Mastery", "Database Design",
            "Cloud Computing", "Artificial Intelligence", "Cybersecurity Handbook",
            "Mobile App Development", "DevOps Practices", "Software Engineering",
            "Network Administration", "System Architecture", "API Design",
            "Frontend Development", "Backend Development", "Full Stack Guide",
            "Agile Methodology", "Project Management", "Code Quality",
            "Testing Strategies", "Performance Optimization", "Scalability Patterns",
            "Microservices Architecture", "Container Technologies", "Serverless Computing",
            "Blockchain Basics", "IoT Fundamentals", "Quantum Computing Intro"
        ]
        types = ['article', 'book', 'misc']
        authors = ["Smith", "Johnson", "Williams", "Brown", "Jones"]

        for i in range(30):
            title = titles[i % len(titles)]
            citation_type = types[i % len(types)]
            author = authors[i % len(authors)]
            year = str(2000 + (i % 25))
            create_citation(title, author, year, citation_type)

        return redirect("/")

from datetime import date
from sqlalchemy import text
from config import db

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, title, author, date FROM citations"))
    citations = result.fetchall()
    return [Citation(citation[0], citation[1], citation[2], citation[3]) for citation in citations]

def create_citation(title, author, date_value):
    sql = text("INSERT INTO citations (title, author, date) VALUES (:title, :author, :date)")
    db.session.execute(sql, { "title": title, "author": author, "date": date(int(date_value), 1, 1) })
    db.session.commit()

def delete_citation(citation_id):
    sql = text("DELETE FROM citations WHERE id = :id")
    db.session.execute(sql, { "id": citation_id })
    db.session.commit()

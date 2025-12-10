from datetime import date
from sqlalchemy import text
from config import db

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("""SELECT id, title, author, date, type,
                                    journal, booktitle, publisher, volume, number, 
                                    pages, editor, edition, institution, note
                                    FROM citations"""))
    citations = result.fetchall()
    return [Citation(citation[0], citation[1], citation[2], citation[3], citation[4], citation[5],
                     citation[6], citation[7], citation[8], citation[9], citation[10], citation[11],
                     citation[12], citation[13], citation[14]) for citation in citations]

def create_citation(title, author, date_value, citation_type,
                    journal=None, booktitle=None, publisher=None, volume=None,
                    number=None, pages=None, editor=None, edition=None,
                    institution=None, note=None):
    sql = text("""INSERT INTO citations (title, author, date, type,
                    journal, booktitle, publisher, volume, number,
                    pages, editor, edition, institution, note)
                    VALUES (:title, :author, :date, :type,
                    :journal, :booktitle, :publisher, :volume, :number,
                    :pages, :editor, :edition, :institution, :note)""")
    db.session.execute(sql, {
        "title": title,
        "author": author,
        "date": date(int(date_value), 1, 1),
        "type": citation_type
        ,"journal": journal,
        "booktitle": booktitle,
        "publisher": publisher,
        "volume": volume,
        "number": number,
        "pages": pages,
        "editor": editor,
        "edition": edition,
        "institution": institution,
        "note": note
    })
    db.session.commit()

# pylint: disable=too-many-locals
def update_citation(citation_id, title, author, date_value, citation_type,
                    journal=None, booktitle=None, publisher=None, volume=None,
                    number=None, pages=None, editor=None, edition=None,
                    institution=None, note=None):
    sql = text("""UPDATE citations
               SET title = :title,
               author = :author,
               date = :date,
               type = :type,
               journal = :journal,
               booktitle = :booktitle,
               publisher = :publisher,
               volume = :volume,
               number = :number,
               pages = :pages,
               editor = :editor,
               edition = :edition,
               institution = :institution,
               note = :note
               WHERE id = :id
               """)
    db.session.execute(sql, {
        "id": citation_id,
        "title": title,
        "author": author,
        "date": date(int(date_value), 1, 1),
        "type": citation_type,
        "journal": journal,
        "booktitle": booktitle,
        "publisher": publisher,
        "volume": volume,
        "number": number,
        "pages": pages,
        "editor": editor,
        "edition": edition,
        "institution": institution,
        "note": note
    })
    db.session.commit()

def delete_citation(citation_id):
    sql = text("DELETE FROM citations WHERE id = :id")
    db.session.execute(sql, { "id": citation_id })
    db.session.commit()

def get_citation(citation_id):
    sql = text("""SELECT id, title, author, date, type, journal, booktitle, publisher,
                          volume, number, pages, editor, edition, institution, note
                          FROM citations WHERE id = :id""")
    result = db.session.execute(sql, { "id": citation_id })
    citation = result.fetchone()
    return Citation(citation[0], citation[1], citation[2], citation[3], citation[4], citation[5],
                    citation[6], citation[7], citation[8], citation[9], citation[10], citation[11],
                    citation[12], citation[13], citation[14])

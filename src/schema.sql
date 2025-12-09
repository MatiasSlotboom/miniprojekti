CREATE TABLE citations (
  id SERIAL PRIMARY KEY, 
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  date DATE NOT NULL,
  type TEXT NOT NULL DEFAULT 'misc',
  journal TEXT,
  booktitle TEXT,
  publisher TEXT,
  volume TEXT,
  number TEXT,
  pages TEXT,
  editor TEXT,
  edition TEXT,
  institution TEXT,
  note TEXT
)
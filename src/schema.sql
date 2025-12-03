CREATE TABLE citations (
  id SERIAL PRIMARY KEY, 
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  date DATE NOT NULL,
  type TEXT NOT NULL DEFAULT 'misc'
)
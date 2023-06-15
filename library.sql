CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(10),
    last_name VARCHAR(20),
    email VARCHAR(30)
);

CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(10) NOT NULL ,
    last_name VARCHAR(20) NOT NULL
);

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL ,
    year_first_published INT
);

CREATE TABLE book_author (
  author_id INT REFERENCES author(id),
  book_id INT REFERENCES book(id)
);

CREATE TABLE bookcopies (
  id SERIAL PRIMARY KEY ,
  book_id INT REFERENCES book(id),
  isbn VARCHAR(13),
  year_published INT
);

CREATE TABLE borrows (
  id SERIAL PRIMARY KEY,
  book_copy_id INT REFERENCES bookcopies(id),
  student_id INT REFERENCES student(id),
  borrowed_data DATE NOT NULL ,
  return_date DATE
);
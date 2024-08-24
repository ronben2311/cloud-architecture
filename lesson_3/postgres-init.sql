CREATE DATABASE lessonFourDB;
\c lessonFourDB
CREATE TABLE mainTable (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO mainTable (name) VALUES ('Initial Data');
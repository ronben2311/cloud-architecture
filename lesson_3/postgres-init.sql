CREATE DATABASE lessonThreeDB;
\connect lessonThreeDB
CREATE TABLE usersTbl (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO usersTbl (name) VALUES ('first user');
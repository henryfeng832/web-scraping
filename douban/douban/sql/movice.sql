CREATE DATABASE douban;

CREATE TABLE top250
(
    id serial NOT NULL,
    title character(100),
    rank real,
    subject character(255),
    duration int2,
    introduction text,
    link text,
    PRIMARY KEY (id)
)

CREATE TABLE ABONENTS(
    abonent_id int primary key,
    abonent_name varchar(255)
);

CREATE TABLE BOOKS(
    book_id int primary key,
    book_title varchar(255),
    abonent_id int,
    foreign key(abonent_id) references ABONENTS(abonent_id)
);
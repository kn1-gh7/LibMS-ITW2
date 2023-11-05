USE library_205;
DROP TABLE IF EXISTS genres, books, users,library_db, transaction_types, lib_transactions, book_genres;

CREATE TABLE genres (
    label INT UNSIGNED,
    categories VARCHAR(40) NOT NULL,
    PRIMARY KEY (label)
);

/*  
	The genre table is more like flag enum for the categories in the books table.
    For example a category = 37 = 0b100101 will mean it belongs to genre 0, 2, and 5    
(0, "Others"),
(1, "Fiction"),
(2, "Mystery"),
(3, "Fantasy"),
(4, "Horror"),
(5, "Nonfiction"),
(6, "Romance"),
(7, "Thriller"),
(8, "Science fiction"),
(9, "Historical fiction"),
(10, "Short story"),
(11, "Literary fiction"),
(12, "Poetry"),
(13, "Graphic novel"),
(14, "Biography"),
(15, "Young adult"),
(16, "Memoir"),
(17, "Dystopia"),
(18, "Magical realism"),
(19, "Children literature"),
(20, "Adventure fiction"),
(21, "Action fiction"),
(22, "Contemporary literature"),
(23, "Paranormal romance"),
(24, "Women fiction"),
(25, "Academic literature")
*/



CREATE TABLE books (
    ISBN VARCHAR(13),
    title VARCHAR(100) NOT NULL,
    author VARCHAR(50),
    -- genre INT UNSIGNED,
    year_published MEDIUMINT UNSIGNED, -- NOTE: THE YEAR DATATYPE IS NOT USED SINCE IT CAN'T STORE YEARS BEFORE 1900s
    description_text VARCHAR(200),
    PRIMARY KEY (ISBN)
);
CREATE TABLE book_genres (
	book_ISBN VARCHAR(13),
    genre INT UNSIGNED,
    foreign key (genre) 
    references genres (label),
    
    foreign key (book_ISBN)
    references books (ISBN)
);
CREATE TABLE users (
    user_id INT UNSIGNED,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id)
);
CREATE TABLE library_db (
    book_id VARCHAR(13),
    total_count INT,
    issued_count INT,
    PRIMARY KEY (book_id),
    FOREIGN KEY (book_id)
        REFERENCES books (ISBN),
    CONSTRAINT not_more_books_issued CHECK ((total_count >= issued_count)
        AND (issued_count >= 0))
); 

CREATE TABLE transaction_types (
    t_type TINYINT,
    t_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (t_type)
);

CREATE TABLE lib_transactions (
    transaction_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    transaction_type TINYINT,
    transaction_time DATETIME,
    the_user_id INT UNSIGNED,
    book_id VARCHAR(13),
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (transaction_type)
        REFERENCES transaction_types (t_type),
    FOREIGN KEY (the_user_id)
        REFERENCES users (user_id),
    FOREIGN KEY (book_id)
        REFERENCES books (ISBN)
);


INSERT INTO genres VALUES (0, "Others"), (1, "Fiction"), (2, "Mystery"), (3, "Fantasy"), (4, "Horror"), (5, "Nonfiction"), (6, "Romance"), (7, "Thriller"), (8, "Science fiction"), (9, "Historical fiction"), (10, "Short story"), (11, "Literary fiction"), (12, "Poetry"), (13, "Graphic novel"), (14, "Biography"), (15, "Young adult"), (16, "Memoir"), (17, "Dystopia"), (18, "Magical realism"), (19, "Children literature"), (20, "Adventure fiction"), (21, "Action fiction"), (22, "Contemporary literature"), (23, "Paranormal romance"), (24, "Women fiction"), (25, "Academic literature");
INSERT INTO books
VALUES
    ('9780451524935', 'To Kill a Mockingbird', 'Harper Lee'    ,  1960, 'A classic novel about racial injustice in the American South.'),
    ('9780141983769', '1984', 'George Orwell'                  ,  1949, 'A dystopian novel depicting a totalitarian society.'),
    ('9780061120084', 'The Catcher in the Rye', 'J.D. Salinger',  1951, 'A coming-of-age novel about a disenchanted teenager.'),
    ('9780062315007', 'The Great Gatsby', 'F. Scott Fitzgerald',  1925, 'A story of wealth, excess, and the American Dream.'),
    ('9780141439563', 'Pride and Prejudice', 'Jane Austen'     ,  1813, 'A romantic novel revolving around the Bennet family.'),
    ('9780451527745', 'Moby-Dick', 'Herman Melville'           ,  1851, 'An epic tale of a man\'s obsession with a white whale.'),
    ('9780060256654', 'Alice\'s Adventures in Wonderland', 'Lewis Carroll',  1865, 'A whimsical fantasy story about a girl named Alice.'),
    ('9780141439594', 'Jane Eyre', 'Charlotte Brontë'          ,  1847, 'A Gothic romance novel featuring the character Jane Eyre.'),
    ('9780451524936', 'The Hobbit', 'J.R.R. Tolkien'           ,  1937, 'A fantasy novel about the adventures of Bilbo Baggins.'),
    ('9780061120060', 'The Lord of the Rings', 'J.R.R. Tolkien',  1954, 'A high-fantasy epic set in the fictional world of Middle-earth.');

INSERT INTO users
VALUES
    (1, 'John Doe'),
    (2, 'Jane Smith'),
    (3, 'Michael Johnson'),
    (4, 'Emily Brown'),
    (5, 'David Wilson'),
    (6, 'Sarah Davis'),
    (7, 'Robert Lee'),
    (8, 'Jennifer Clark'),
    (9, 'William White'),
    (10, 'Elizabeth Martin');
    
INSERT INTO library_db
VALUES
    ('9780451524935', 10, 3),
    ('9780141983769', 8, 2),
    ('9780061120084', 15, 5),
    ('9780062315007', 12, 4),
    ('9780141439563', 7, 1),
    ('9780451527745', 9, 2),
    ('9780060256654', 11, 3),
    ('9780141439594', 6, 1),
    ('9780451524936', 10, 3),
    ('9780061120060', 14, 4);

INSERT INTO transaction_types 
VALUES
	(1, "book issued"),
	(2, "book returned");
    
INSERT INTO lib_transactions (transaction_id, transaction_type, transaction_time, the_user_id, book_id)
VALUES
    (1, 1, '2023-09-18 10:00:00', 1, '9780451524935'),
    (2, 1, '2023-09-19 11:30:00', 2, '9780141983769'),
    (3, 1, '2023-09-20 14:15:00', 3, '9780061120084'),
    (4, 2, '2023-09-21 16:45:00', 1, '9780451524935'),
    (5, 2, '2023-09-22 09:20:00', 2, '9780141983769'),
    (6, 1, '2023-09-23 13:10:00', 4, '9780062315007'),
    (7, 2, '2023-09-24 17:30:00', 3, '9780061120084');

delimiter |
CREATE TRIGGER count_check BEFORE INSERT ON lib_transactions
	FOR EACH ROW
		BEGIN
			IF NEW.transaction_type =  1 THEN
				UPDATE library_db
				SET library_db.issued_count = library_db.issued_count + 1
				WHERE NEW.book_id = library_db.book_id;
			ELSEIF NEW.transaction_type =  2 THEN
				UPDATE library_db
				SET library_db.issued_count = library_db.issued_count - 1
				WHERE NEW.book_id = library_db.book_id;
			END IF;
		END;
|
delimiter ;

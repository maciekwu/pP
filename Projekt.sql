#create database projektt;
use projektt;
SET FOREIGN_KEY_CHECKS = 0;
drop table IF EXISTS Uzytkownicy;
drop table IF EXISTS Miejsca;
drop table IF EXISTS Relacje;
drop table IF EXISTS Wiadomosci;
drop table IF EXISTS Ocena;
drop table IF EXISTS Lokacja;
drop table IF EXISTS Logowanie;

drop VIEW IF EXISTS userInLocationRating;
drop VIEW IF EXISTS messageAuthorRead;
drop trigger IF EXISTS t_deleteUser;

create table Uzytkownicy (
    id INT AUTO_INCREMENT,
    imie VARCHAR(25) NOT NULL,
	miasto VARCHAR(35) NOT NULL,
    mail VARCHAR(100) NOT NULL UNIQUE ,
	PRIMARY KEY (id)
    );
    
create table Miejsca (
    id INT AUTO_INCREMENT,
    nazwa VARCHAR(25) NOT NULL unique,
	miasto VARCHAR(35) NOT NULL DEFAULT 'Warszawa',
	PRIMARY KEY (id)
    );
    
create table Relacje (
    id INT AUTO_INCREMENT,
    typ_relacji VARCHAR(25) NOT NULL, 
    id_user INT NOT NULL,
    id_friend INT NOT NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_friend) REFERENCES Uzytkownicy (id),
	CONSTRAINT UQ_relation UNIQUE NONCLUSTERED (id_user, id_friend)
    );
    
create table Wiadomosci (
    id INT AUTO_INCREMENT,
    tresc VARCHAR(300) NOT NULL,
    id_user INT NOT NULL,
    id_friend INT NOT NULL,
    is_read CHAR NOT NULL DEFAULT '0',
	PRIMARY KEY (id),
	FOREIGN KEY (id_user) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_friend) REFERENCES Uzytkownicy (id)
    );
    
create table Lokacja ( 
    id INT AUTO_INCREMENT,
    id_user INT NOT NULL,
    id_place INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_user) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_place) REFERENCES Miejsca (id),
    CONSTRAINT UQ_location UNIQUE NONCLUSTERED (id_user, id_place)
    );
    
create table Ocena ( 
    id INT AUTO_INCREMENT,
    ocena INT NOT NULL,
    komentarz VARCHAR(300),
    id_user INT NOT NULL,
    id_place INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_user) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_place) REFERENCES Miejsca (id),
	CONSTRAINT UQ_rating UNIQUE NONCLUSTERED (id_user, id_place)
    );
    
create table Logowanie ( 
    id INT AUTO_INCREMENT,
    mail VARCHAR(300) NOT NULL unique,
    passwrd VARCHAR(300) NOT NULL,
    id_user INT NOT NULL unique,
	PRIMARY KEY (id),
	FOREIGN KEY (id_user) REFERENCES Uzytkownicy (id)
    );


CREATE VIEW userInLocationRating AS (
	select 
	u.mail as mail, 
	case when m.nazwa is null then 'is Unchecked' else concat('has checked-in to: ', m.nazwa) end as where_is,
	o.ocena as rating 
	from uzytkownicy u 
	left join lokacja l on l.id_user = u.id 
	left join miejsca m on m.id = l.id_place 
	left join ocena o on o.id_user = l.id_user and o.id_place = l.id_place
);

CREATE VIEW messageAuthorRead AS (
	select 
    u.mail as recipient, 
    u1.mail as author,
	w.tresc as content,
	w.is_read as is_read
	from wiadomosci w 
	join uzytkownicy u on u.id = w.id_friend
    join uzytkownicy u1 on u1.id = w.id_user

);

/*
CREATE TRIGGER t_deleteUser
after delete ON logowanie-- zdarzenie określające kiedy trigger zostanie wyzwolony
 -- tabela na której triger zostanie założony
FOR EACH ROW 
	BEGIN
     DELETE FROM relacje WHERE id_user = (SELECT id FROM uzytkownicy WHERE mail = 'mck');
	-- skrypt wykonywany przez triger
	END;

*/



-- TODO: kursory uruchamiane przy usuwaniu konta - czyszczą pozostałe tabele: logowanie, wiadomości, relacje
-- TODO: trigger dla usuwania znajomego (relacja, wiadomosci)
-- TODO: napisz constraint na tabeli wiadomości - > przy tworzeniu nowego rekordu id_user != id_friend
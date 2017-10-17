#create database projektt;
use projektt;
SET FOREIGN_KEY_CHECKS = 0;
drop table Uzytkownicy;
drop table Miejsca;
drop table Relacje;
drop table Wiadomosci;
drop table Ocena;
drop table Lokalizacja;
drop table Logowanie;
drop trigger t_logowanie;

create table Uzytkownicy (
    id INT AUTO_INCREMENT,
    imie VARCHAR(25) NOT NULL,
    #nazwisko VARCHAR(35) NOT NULL,
	miasto VARCHAR(35) NOT NULL,
    #plec VARCHAR(35) NOT NULL,
    mail VARCHAR(100) NOT NULL unique,
	PRIMARY KEY (id)
    );
    
create table Miejsca (
    id INT AUTO_INCREMENT,
    nazwa VARCHAR(25) NOT NULL unique,
    ulica VARCHAR(35) NOT NULL,
    nr_lokalu int,
	miasto VARCHAR(35) NOT NULL,
	PRIMARY KEY (id)
    );
    
create table Relacje (
    id INT AUTO_INCREMENT,
    typ_relacji VARCHAR(25) NOT NULL, 
    id_u INT NOT NULL,
    id_z INT NOT NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (id_u) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_z) REFERENCES Uzytkownicy (id)
    );
    
create table Wiadomosci (
    id INT AUTO_INCREMENT,
    tresc VARCHAR(300) NOT NULL,
    id_u INT NOT NULL,
    id_z INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_u) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_z) REFERENCES Uzytkownicy (id)
    );
    
create table Lokalizacja ( 
    id INT AUTO_INCREMENT,
    id_u INT NOT NULL,
    id_m INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_u) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_m) REFERENCES Miejsca (id)
    );
    
create table Ocena ( 
    id INT AUTO_INCREMENT,
    ocena INT NOT NULL,
    komentarz VARCHAR(300),
    id_u INT NOT NULL,
    id_m INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_u) REFERENCES Uzytkownicy (id),
    FOREIGN KEY (id_m) REFERENCES Miejsca (id)
    );
    
create table Logowanie ( 
    id INT AUTO_INCREMENT,
    mail VARCHAR(300) NOT NULL unique,
    passwrd VARCHAR(300) NOT NULL,
    id_u INT NOT NULL unique,
	PRIMARY KEY (id),
	FOREIGN KEY (id_u) REFERENCES Uzytkownicy (id)
    );
    
drop trigger t_logowanie;

-- create trigger t_logowanie
-- before delete on uzytkownicy
-- 	delete from logowanie where uzytkownicy.id = logowanie.id_u 
-- TODO: kursory dla usuwania konta
-- TODO: constraint na pary unikalne w tabeli relacja
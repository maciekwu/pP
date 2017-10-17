use projektt;
select * from Uzytkownicy;
select * from Logowanie;
select * from Relacje;
select * from Miejsca;
select * from Wiadomosci;
select * from Ocena;
select * from Lokalizacja;


alter table uzytkownicy drop column plec;
alter table uzytkownicy add column 	miasto VARCHAR(35) NOT NULL;



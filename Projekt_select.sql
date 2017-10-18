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


INSERT INTO Relacje (TYP_RELACJI, ID_U, ID_Z) values ('F', (select id from Uzytkownicy where mail = 'mck'), (select id from Uzytkownicy where mail = 'krk'));


select mail from uzytkownicy where id in (select id_z from relacje where id_u = (select id from uzytkownicy where mail = 'mck'));
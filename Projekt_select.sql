use projektt;
select * from Uzytkownicy;
select * from Logowanie;
select * from Relacje;
select * from Miejsca;
select * from Lokacja;
select * from Wiadomosci;
SELECT * FROM Ocena;





select mail from uzytkownicy where id in (select id_z from relacje where id_u = (select id from uzytkownicy where mail = 'mck'));
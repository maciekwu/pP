insert into Logowanie 
(mail, passwrd, id_u)
values
('mckkkk', 'aaa', (select id from Uzytkownicy where mail = 'mckkkk'));

delete from Logowanie;
delete from uzytkownicy;
delete from relacje;


select * from relacje where id_u = (select id from uzytkownicy where mail = 'mck') and id_z = (select id from uzytkownicy where mail = 'plp');
insert into Logowanie 
(mail, passwrd, id_u)
values
('mckkkk', 'aaa', (select id from Uzytkownicy where mail = 'mckkkk'));

delete from Logowanie;
delete from uzytkownicy;
delete from relacje;
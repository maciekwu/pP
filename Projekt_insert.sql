insert into Logowanie 
(mail, passwrd, id_u)
values
('mckkkk', 'aaa', (select id from Uzytkownicy where mail = 'mckkkk'));



insert into miejsca (nazwa)  values ('Lustra');
insert into miejsca (nazwa)  values ('Smolna');
insert into miejsca (nazwa)  values ('Szwejk');
insert into miejsca (nazwa)  values ('Kulturalna');
insert into miejsca (nazwa)  values ('Parana');
insert into miejsca (nazwa)  values ('Mc Donald\'s');
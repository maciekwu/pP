

insert into miejsca (nazwa)  values ('Lustra');
insert into miejsca (nazwa)  values ('Smolna');
insert into miejsca (nazwa)  values ('Szwejk');
insert into miejsca (nazwa)  values ('Kulturalna');
insert into miejsca (nazwa)  values ('Parana');
insert into miejsca (nazwa)  values ('Mc Donald');



INSERT INTO relacje (TYP_RELACJI, id_user, id_friend) values ('F', (select id from Uzytkownicy where mail = 'mck'), (select id from Uzytkownicy where mail = 'krk'));

insert into wiadomosci (tresc, id_user, id_friend) values ('%100s', (select id from Uzytkownicy where mail = '%s'), (select id from Uzytkownicy where mail = '%s'));



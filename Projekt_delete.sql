delete from Logowanie;

delete from uzytkownicy;

delete from relacje;

DELETE FROM lokacja WHERE id_u = (SELECT id FROM uzytkownicy WHERE mail = '%s');
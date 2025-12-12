## Ohtu miniprojekti

[![CI](https://github.com/MatiasSlotboom/miniprojekti/actions/workflows/ci.yaml/badge.svg)](https://github.com/MatiasSlotboom/miniprojekti/actions/workflows/ci.yaml)

## Backlog
Product/Sprint Backlog löytyy täältä -> [backlog](https://docs.google.com/spreadsheets/d/1EQwYgxdFO3TrHe9c7N8aJtbnicHo_mB4gMRst7pz7TI/edit?gid=860632009#gid=860632009).

## Sovelluksen asennus- ja käyttöohje
Lisää sovelluksen juureen .env-tiedosto, jonka sisältö on
```
DATABASE_URL=postgresql://xxx
TEST_ENV=true
SECRET_KEY=satunnainen_merkkijono
```
Asenna sovelluksen riippuvuudet:
```
$ poetry install
```
Siirry Poetry-virtuaaliympäristöön:
```
$ eval $(poetry env activate)
```
Alusta sovelluksen tietokanta ennen sovelluksen ensimmäistä käynnistämistä:
```
$ python src/db_helper.py
```
Käynnistä sovellus:
```
$ python src/index.py
```
Yksikkötestit voi suorittaa komennolla:
```
$ pytest src/tests
```
Robot-testit voi suorittaa komennolla:
```
$ robot src/story_tests
```

## Definition of done
- [x] Koodi on siistiä ja ymmärrettävää.
- [x] Sovellus ei aiheuta virheilmoituksia normaalissa käytössä.
- [x] Testit menevät läpi ja ne suoritetaan onnistuneesti GitHub Actionsissa.
- [x] Hyväksymiskriteerit täyttyvät
- [x] README-tiedosto on ajantasalla.

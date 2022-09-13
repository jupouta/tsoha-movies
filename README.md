# Tietokantasovellus: Elokuvasovellus

Sovelluksessa voi lukea elokuva-arvosteluja ja elokuvien saamia arvioita sekä elokuvien perustietoja.
Käyttäjä on joko peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan elokuvista sekä elokuvalle annettujen arvioiden keskiarvon.
- Käyttäjä voi painaa elokuvan nimeä, jolloin siitä näytetään lisätietoja (esim. ohjaaja, valmistumisvuosi) ja käyttäjien sille antamat kirjalliset arviot.
- Käyttäjä voi antaa arvion (numeerinen ja mahdollinen kirjallinen arvio) elokuvasta ja lukea muiden antamia arvioita.
- Ylläpitäjä voi lisätä ja poistaa elokuvia sekä määrittää elokuvasta näytettävät tiedot.
- Käyttäjä voi etsiä kaikki elokuvat, joiden nimessä on annettu sana.
- Käyttäjä näkee myös listan, jossa elokuvat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.

## Python + docker

    docker-compose up
    docker-compose down

Python

    pip freeze > requirements.txt
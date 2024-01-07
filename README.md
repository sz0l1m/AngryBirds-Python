# PIPR-PROJECT

## Autor
Miłosz Andryszczuk
nr indeksu 331355

## Opis projektu
Przedmiotem projektu jest gra 2D w stylu Angry Birds. Gra polega na wystrzeleniu ptaka pod odpowiednim kątem i z odpowiednią siłą, tak aby trafił on bezpośrednio w cele, czyli świnie lub w konstrukcje, których zawalenie spowoduje zlikwidowanie świni. Gra składa się z kilku poziomów o narastającym poziomie trudności. Projekt posiada interfejs graficzny oraz potrafi symulować prawa fizyki.<br>
Projekt wykorzytuje 2 biblioteki spoza standardowej biblioteki Pythona:
- Pygame<br>
Odpowiada za interfejs graficzny gry, wyświetlając wszystkie elementy na ekranie.<br>
[Dokumentacja](https://www.pygame.org/docs/)
- Pymunk<br>
Odpowiada za symulacje fizyki wszystkich obiektów w grze.<br>
[Dokumentacja](https://www.pymunk.org/en/latest/index.html)


## Struktura projektu
- Folder **src**<br>
Główny folder zawierający logikę gry: funkcje, klasy i ich metody wykorzystywane w grze.
    - `get_levels.py`<br>
    Zawiera klasę Game oraz Level.
    - `classes.py`<br>
    Zawiera klasy wszystkich obiektów wyświetlanych w grze, własne błędy oraz funkcje wykorzystywane przez klasy.
    - `collisions.py`<br>
    Zarządza kolizjami pomiędzy obiektami i na podstawie energii uderzenia decyduje, kiedy obiekty powinny zniknąć.
- Folder **setup**<br>
Zawiera pliki konfiguracyjne, które pozwalaja na szybką zmianę parametrów i ustawień gry.
    - `levels.json`<br>
    Zawiera dane o położeniu i wielkości obiektów w poszczególnych poziomach zapisane w formacie *JSON*.
    - `colors.py`<br>
    Zawiera wszytkie kolory wykorzystywane w grze.
    - `config.py`<br>
    Zawiera globalne zmienne, takie jak na przykład liczba klatek na sekundę czy rozmiar ptaka. Oblicza również wielkość ekranu gry.
- Folder **tests**
    - `test_classes.py`<br>
    Zawiera testy klas i funkcji z pliku `classes.py`.
    - `test_get_levels.py`<br>
    Zawiera testy klas z pliku `get_levels.py`.
- Folder **images**
    - Zawiera obrazy wykorzystywane w grze w formacie *png* lub *jpg*.
- `game.py`<br>
Główny plik całej gry. Tworzy instancje klasy Game i wywołuje jej metody.<br>
Uruchomienie tego pliku powoduje włączenie gry.
- `requirements.txt`<br>
Zawiera biblioteki niezbędne do poprwanego działania gry.
-  `.gitignore`<br>
Zawiera informacje o plikach i folderach ignorowanych przez *git*.
- `README.md`<br>
Zawiera opis projektu i instrukcje użytkowania.

## Podział na klasy
- **Game**<br>
Główna klasa, która łączy wszystkie klasy w całość. Stworzenie jej instancji jest równoznaczne z odpaleniem gry i powoduje uruchomienie biblioteki pygame (tym samym urochomienie okna gry), załadowanie używanych obrazów i ustawienie domyślnych wartości atrybutów. Jej metody wywoływane co każdą klatkę pozwalają na wyświetlenie obrazu startowego i końcowego, rysowanie obiektów na ekranie, aktualizowanie położenia obiektów, restartowanie poziomu, wczytywanie kolejnego poziomu, wczytywanie kolejnej próby, a także reagowanie na położenie myszki czy na przyciski wciśnięte przez gracza. Klasa jest również odpowiedzialna za utrzymanie odpowiedniej częstotliwości wyświetlania klatek oraz za wiele innych funkcjonalności.

- **Level**<br>
Klasa ta jest odpowiedzialna za wczytanie poziomu z pliku oraz zapisanie informacji o nim, takich jak np. liczba prób. Poza tym pozwala na stworzenie wszystkich obiektów potrzebnych do stworzenia poziomu poprzez stworzenie instancji odpowiednich klas z pliku `classes.py`.

- **Bird**<br>
Klasa ta reprezentuje ptaka, którym można strzelać. Posiada atrybuty dotyczące kształtu, wielkości, wyglądu, położenia, prędkości, masy i innych cech potrzebnych do symulacji fizyki. Oblicza kąt i prędkość z jaką ptak zostanie wystrzelony na podstawie położenia myszki lub wciśniętych klawiszy.

- **Trajectory**<br>
Klasa ta pozwala na obliczenie i wyświetlenie trajektorii ptaka na podstawie prędkości i kątu ustawionego przez gracza. Do narysowania trajektorii oblicza współczynniki funkcji kwadratowej, która reprezentuje tą trajektorię.

- **Pig**<br>
Klasa ta reprezentuje świnie, czyli cele, w które trzeba trafić. Posiada podobne atrybuty jak *Bird* niezbędne do narysowania świni i symulowania jej fizyki.

- **Bar**<br>
Klasa ta reprezentuje belkę, z których można budować konstrukcje. Pozwala na stworzenie belki statycznej, która się nie porusza i belki dynamicznej, która reaguje na zderzenia z innymi obiektami i może się przemieszczać.

- **Wooden_bar**<br>
Klasa ta dziedziczy wszystkie atrybuty i metody po klasie *Bar* i nadpisuje niektóre atrybuty. Jest to rodzaj belki dynamicznej, która jest stosunkowo lekka i może ulec zniszczeniu po zderzniu z wystarczającą energią kinetyczną z innym obiektem.

- **Stone_bar**<br>
Klasa ta podobnie jak klasa *Wooden_bar* dziedziczy po klasie *Bar*. Jest to również rodzaj belki dynamicznej, która może się poruszać, jednak w odróznieniu od belki drewnianej, belka ta ma inne parametry fizyczne i nigdy nie ulega zniszczeniu po zderzeniu z innymi obiektami.

- **Floor**<br>
Klasa ta reprezentuje podłogę danego poziomu. Podobnie jak inne klasy reprezentujące obiekty posiada parametry fizyczne dotyczące kształtu, elastyczności itp.

- **Skin**<br>
Klasa ta reprezentuje 'skórki' wykorzystywane przez obiekty, czyli obrazy, które są wyświetlane na ekranie w miejscu tych obiektów. Klasa pobiera obrazy z folderu images i kompresuje je do opowiedniego rozmiaru.

- **Text**<br>
Klasa ta reprezentuje teksty wykorzystywane w grze. Poza samym tekstem pozwala na ustawienie takich atrybutów jak: położenie, rozmiar, kolor i czcionka.

- **CoordinatesError** i **SizeError**<br>
Klasy te reprezentują błędy, które są zgłaszane kiedy podane dane są nieprawidłowe.<br>

## Instrukcja użytkowania ##

### Instalacja ###
Należy stworzyć folder, w którym gra będzie zapisana i sklonować repozytorium do tego folderu. Pliki gry znajdujować się będą w nowym folderze `23Z-PIPR-PROJECT-Andryszczuk-Milosz`.
```
mkdir game
cd game
git clone https://gitlab-stud.elka.pw.edu.pl/23z-pipr/project/204mm/23Z-PIPR-PROJECT-Andryszczuk-Milosz.git
cd 23Z-PIPR-PROJECT-Andryszczuk-Milosz
```
Warto upewnić się, czy w folderze tym znajdują się pliki opisane powyżej w sekcji *struktura plików*.<br>
Następnie należy pobrać wymagane biblioteki z pliku `requirements.txt`.
```
pip install -r requirements.txt
```
Po pomyślnym zainstalowaniu bibliotek grę można uruchomić za pomocą komendy:

```
python3 game.py
```

### Instrukcja rozgrywki ###
Po uruchomieniu gry powinno pojawić się okno z ekranem startowym.<br>

W każdym momencie grę można wyłączyć klikając przycisk `escape` lub `x` w prawym górnym rogu ekranu.

Po kliknięciu `spacji` załaduje się pierwszy poziom.<br>

**Strzelanie ptakiem**:<br>

Ptaka można wystrzelić pod każdym kątem, jednak siła wystrzału jest ograniczona. Zależnie od wybranych parametrów pokazywać się będzie kawałek trajketorii, po której ptak będzie leciał.<br>

Kąt oraz siłę wystrzału ptaka można dobrać na 2 sposoby:<br>
- Myszka<br>
Po naciśnięciu na ptaka ``lewym przyciskiem myszy`` można zmieniać kąt i siłę wystrzału przesuwając kursor dookoła niego. ``Puszczenie lewego przycisku`` lub naciśnięcie `spacji` spowoduje wystrzelenie ptaka.<br>
Po naciśnięciu ptaka można nacisnąć ``prawy klawisz myszy`` aby go puścić bez wystrzelania go.

- Klawiatura<br>
Siłę i kąt wystrzelania ptaka można również zmieniać za pomocą przycisków `WASD` lub `strzałek`.
    - `W` lub `UP` - zwiększenie kąta
    - `S` lub `DOWN` - zmniejszenie kąta
    - `D` lub `RIGHT` - zwiększenie prędkości
    - `A` lub `LEFT` - zmniejszenie prędkości<br>
Aby wystrzelić ptaka z wybranymi parametrami należy nacisnąc `spację`.

**Pozostałe sterowanie**<br>

`R` - restart aktualnego levelu.<br>
`SPACJA` - załadowanie kolejnej próby przed zatrzymaniem się wszytkich obiektów (działa o ile w aktualnej próbie ptak został już wystrzelony i są dostępne jeszcze kolejne próby).<br>
`ESCAPE` - wyłączenie gry.

**Cel rozgrywki**<br>

Gra polega na dobraniu takiej trajektorii, aby ptak trafił bezpośrednio w świnie lub w konstrukcje, których zawalenie się spowoduje zabicie świń. Po oddanym strzale, jeśli jakieś świnki pozostały jeszcze przy życiu następuje kolejna próba. Każdy level ma ograniczoną liczbę prób, których wyczerpanie przed zabiciem wszystkich świń powoduje automatyczny restart poziomu. Po zlikwidowaniu wszystkich świń gra przechodzi do następnego poziomu.

Zrestartować level oraz załadować kolejną próbę można również samodzielnie za pomocą przycisków opisancyh wyżej w sekcji *pozostałe sterowanie*.


## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.
 Ptaka można wystrzelić pod każdym kątem, jednak siła wystrzału jest ograniczona. Zależnie od położenia myszki pokazywać się będzie kawałek trajketorii, po której ptak będzie leciał.
## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

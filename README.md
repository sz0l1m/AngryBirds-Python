# Angry Birds

## Autor
Miłosz Andryszczuk
nr indeksu 331355

## Opis projektu
Przedmiotem projektu jest gra 2D w stylu Angry Birds. Gra polega na wystrzeleniu ptaka pod odpowiednim kątem i z odpowiednią siłą, tak aby trafił on bezpośrednio w cele, czyli świnie lub w konstrukcje, których zawalenie spowoduje zlikwidowanie świni. Gra składa się z szęsciu poziomów o narastającym poziomie trudności. Projekt posiada interfejs graficzny oraz potrafi symulować prawa fizyki.<br>
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
Główna klasa, która łączy wszystkie klasy w całość. Stworzenie jej instancji jest równoznaczne z odpaleniem gry i powoduje uruchomienie biblioteki pygame (tym samym uruchomienie okna gry), załadowanie używanych obrazów i ustawienie domyślnych wartości atrybutów. Jej metody wywoływane co każdą klatkę pozwalają na wyświetlenie obrazu startowego i końcowego, rysowanie obiektów na ekranie, aktualizowanie położenia obiektów, restartowanie poziomu, wczytywanie kolejnego poziomu, wczytywanie kolejnej próby, a także reagowanie na położenie myszki czy na przyciski wciśnięte przez gracza. Klasa jest również odpowiedzialna za utrzymanie odpowiedniej częstotliwości wyświetlania klatek oraz za wiele innych funkcjonalności.

- **Level**<br>
Klasa ta jest odpowiedzialna za wczytanie poziomu z pliku oraz zapisanie informacji o nim, takich jak np. liczba prób. Poza tym pozwala na stworzenie wszystkich obiektów danego poziomu poprzez stworzenie instancji odpowiednich klas z pliku `classes.py`.

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
Należy stworzyć folder, w którym gra będzie zapisana i sklonować repozytorium do tego folderu. Pliki gry znajdować się będą w nowym folderze `23Z-PIPR-PROJECT-Andryszczuk-Milosz`.
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

Po przejściu wszytkich poziomów wyświetli się ekran końcowy z łącznym czasem rozgrywki. Grę można uruchomić ponownie poprzez `spacje` lub wyłączyć za pomocą `escape`.

### Modyfikacja gry ###

Poziomy gry zapisane są w formacie `JSON` w pliku `levels.json`. Każdy poziom ma swój numer i obiekty, które się w nim znjadują, czyli świnki i belki. Możliwa jest modyfikacja stworzoncyh leveli oraz dodawanie nowych. Każdy obiekt ma swoją pozycję zapisaną w pixelach oraz promień (dla świnek) lub rozmiar w dwóch wymiarach (dla belek) również w pixelach. W belkach w kluczu `type` można wybrać czy ma byc ona statyczna, drewniana lub kamienna (brak klucza `type` oznacza, że belka jest drewniana). W kluczu `bird` `amount` można dobrać liczbę prób. Przy modyfikacji poziomów należy pamiętać, że:
- pozycja obiektu wskazuje, gdzie znajdować się będzie środek obiektu
- pozycja pozioma `x_position` liczona jest od prawej krawędzi ekranu
- nie należy podawać wartości ujemnych oraz `x_position` większego niż 1900 oraz `y_postion` większego niż 1000<br>
- po dodaniu lub usunięciu levelu należy pamiętać o zmodyfikowaniu numerów leveli

Trzymanie się powyższych zasad pozwala na łatwe modyfikowanie poziomów wedle uznania.


## Część refleksyjna

### Potencjalne probelmy ###

**Ekran**<br>
Możliwe jest, że na Pańskim ekranie gra nie będzie wyświetlać się prawidłowo. Gra była tworzona na ekranie o rozmiarach 1920 x 1200 pixeli i zadbałem o to, żeby ekran, i grafika dopasowywała się do każdego ekranu, jednak z powodu ograniczonego dostępu do innych monitorów nie byłem w stanie w pełni tego przetestować. Testowałem to łącznie na 4 komputerach i wszystko działało prawidłowo, jednak mimo to radziłbym, aby urochomić tą grę mając włączony tylko jeden monitor (jeśli korzysta Pan z kilku), ponieważ czasami w przypdaku używania dwóch monitorów okno gry wychodziło częściowo na drugi ekran.

**Poziom trudności**<br>
Ciężko jest ocecnić poziom trudności tej gry, ponieważ przeszedłem ją kilkadziesiąt razy i według mnie nie jest trudna. Przez długi czas starałem się zbalansować tą grę, aby była jak najbardziej zbalansowana. Natomiast jeśli będzie miał Pan trudności z jej przejściem, to zachęcam do zmodyfikowania lub nawet usunięcia danego levelu zgodnie z intrukcją powyżej.

### Niezrealizowane pomysły ###

- stworzenie różnych rodzajów ptaków (jak w prawdziwym Angry Birds)
- dodanie instrukcji użytkowania w grze
- dodanie prostych animacji po zabiciu świń lub zniszczeniu belek (coś w stylu wybuchów)
- dodanie innych rodzajów belek (np. szklancyh)
- dodanie inncyh kształtów belek (trójkątów, kół, itd)
- dodanie efektów dźwiękowych i muzyki
- dodanie większej ilości poziomów
- i wiele wiele innych<br>

Wszytkie powyższe pomysły nie zostały zrealizowane z powodu ograniczenia czasowego i z pewnością zostały by zaimplemenotwane, gdyby nie termin.

### Zakończenie ###
Mimo dużej ilości niezrealizowanych pomysłów, to jednak lista tych zrealizowanych, których początkowo kompletnie nie było w planie, jest znacznie dłuższa. Początkowo myślałem o grze, której "grafika" będzie symulowana w konsoli, a jedyna fizyka to będzie kropeczka poruszająca się po paraboli. A jednak udało się stworzyć grę, o której nigdy nie pomyslałbym, że jest w moim zasięgu.

Podczas pisania tego projektu poświęciłem mnóstwo czasu, żeby poznać i nauczyć się korzystać z wykorzystywanych przeze mnie bibliotek i natrafiłem na niezliczoną ilość problemów i błędów, jednak dzięki temu nauczyłem się lepszej organizacji kodu oraz korzytania z bardzo rozbudowanych i przydatnych bibliotek a także dowiedziałem się jak wiele można dzięki nim osiągnąć.

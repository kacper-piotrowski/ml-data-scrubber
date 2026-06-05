# ML-DataScrubber
Projekt ma na celu umożliwić łatwe operacje na plikach
wykorzystywanych później do uczenia modeli Machine Learning. Jest to aplikacja GUI
która wspiera oczyszczanie, analizowanie i przygotowywanie danych w formatach
CSV, TXT oraz JSON.

## Główne funkcjonalności:
- Wczytywanie danych (obsługa CSV z nagłówkami lub bez)
- Statystyki słów: Wypisanie liczby unikalnych wyrazów wraz z wypisaniem ich listy,
oraz generowanie wykresu 10 najczęstszych słów
- Filtrowanie danych: usuwanie zbyt krótkich wierszy danych z parametrem długości użytkownika
- Cenzurowanie danych: predefiniowane regexy dla adresów e-mail, numerów pesel oraz polskich
numerów telefonów, które maskują dane wrażliwe
- Podział na pliki do treningu: losowe mieszanie danych i eksport batchy o podanej wielkości przez użytkownika
przy pomocy generatora

## Wykorzystane biblioteki:
- Standardowe biblioteki Python: `json`, `csv`, `re`, `random`, `pathlib`, `time`, `functools`
- Biblioteki zewnętrzne:
- - `customtkinter` - używana do stworzenia interfejsu graficznego
- - `matplotlib` - używana do dynamicznego rysowania wykresów częstości słów

## Struktura projektu:
- `main.py` - Uruchamia, pętlę GUI
- `gui.py` - Definicja interfejsu użytkownika, oraz obsługa zdarzeń logicznych i interakcji
- `engine.py` - Logika działania wszystkich funkcji programu oraz definicja klas Dataset i TextDataset
- `utils.py` - Zawiera wszystkie customowe wyjątki, oraz dekorator do logowania czasu wykonania funkcji

## Instrukcja uruchomienia:
1. Wypakowanie projektu
2. Instalacja bibliotek:
```bash
pip install customtkinter matplotlib
 ```
3. Uruchomienie aplikacji:
```bash
python main.py
```

## Własne wyjątki:
- BadRowException - rzucany, gdy w wiersz w pliku CSV ma niepoprawną liczbę kolumn
- NoDatasetException - rzucany, kiedy brakuje nam danych do wykonania pewnej logiki
- InvalidBatchNumberException - rzucany, gdy rozmiar batcha przekracza liczbę wszystkich wierszy
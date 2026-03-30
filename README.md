# Sports Event Calendar

Prosta aplikacja webowa do zarządzania meczami sportowymi. Pozwala przeglądać, dodawać i filtrować mecze po dacie.

## Przegląd projektu

Aplikacja składa się z trzech głównych części:

1. **Baza danych SQLite** - przechowuje mecze, drużyny, ligi i etapy turnieju
2. **Backend FastAPI** - REST API z endpointami do pobierania i dodawania meczy
3. **Frontend HTML + JavaScript** - interfejs webowy do wyświetlania i filtrowania meczy

## Technologia

- **Backend:** FastAPI (Python)
- **Baza danych:** SQLite 3
- **Frontend:** HTML, CSS, JavaScript
- **Wersjonowanie:** Git

## Wymagania funkcjonalne 

**Task 1 - Modelowanie bazy danych**
- Zaprojektowana baza z 4 tabelami: `competitions`, `stages`, `teams`, `events`
- Relacje one-to-many między tabelami
- Normalizacja 3NF 
- Powiązania między tabelami oznaczane underscore'em

**Task 2 - Struktura i dane**
- Baza danych SQLite z 8 załadowanymi meczami
- Poprawne PK i FK
- 8 meczy, 9 drużyn, 1 liga (AFC Champions League), 2 etapy (ROUND OF 16, FINAL)

**Task 3 - Implementacja**

**Backend:**
- GET `/events` - lista wszystkich meczy z informacją o drużynach (single SQL query z JOINami)
- GET `/events/{event_id}` - szczegóły jednego meczu
- GET `/competitions` - lista dostępnych lig
- POST `/events` - dodawanie nowego meczu
- GET `/` - zwraca stronę HTML

**Frontend:**
- Tabela ze wszystkimi meczami
- Filtrowanie po dacie
- Formularz do dodawania meczu
- Stylowanie CSS
- Auto-refresh po dodaniu nowego meczu

## Założenia i decyzje projektowe

### 1. Baza danych
- **SQLite zamiast MySQL/PostgreSQL** - prostsze do deployment'u, plik lokalny
- **LEFT JOIN zamiast pętli SQL** - wymaganie zadania
- **Foreign keys z prefixem underscore** - powiązania do innych tabel oznaczane (_) np. `_home_team_id`, `_away_team_id` dla przejrzystości 

### 2. Status meczu i wynik
- **Zaplanowany** - wynik = NULL ponieważ, mecz się jeszcze nie odbył
- **Rozegrany** - wynik zawsze podany
- Frontend wyłącza pola wyniku gdy status = zaplanowany

### 3. Drużyny w dodawaniu meczu
- Użytkownik wpisuje nazwę drużyny
- Backend szuka drużyny po nazwie i przypisuje ID
- Jeśli drużyna nie istnieje w bazie - ustawia NULL

### 4. Frontend
- **Bez frameworku** - prostszy HTML/CSS/JS dla przejrzystości
- **Fetch API** - komunikacja z backendem
- **Filtrowanie po stronie klienta** - wszystkie dane pobieramy raz, filtrowanie bez dodatkowych zapytań do API

### 5. Struktura projektu
```
project/
├── app.py             # Backend (FastAPI)
├── database.py        # Schemat i inicjalizacja bazy
├── load_data.py       # Załadowanie danych z JSON
├── clean_json.py      # Czyszczenie JSON z błędów OCR
├── data.json          # Dane meczy
├── requirements.txt   # Zależności
├── templates/
│   └── index.html     # Frontend
├── .gitignore         # Ignoruj cache i bazę danych
└── sports_calendar.db # Baza SQLite
```

## Instrukcja instalacji i uruchomienia

### 1. Wymagania
- Python 3.8+
- pip (package manager)

### 2. Klonowanie repozytorium
```bash
git clone https://github.com/KaSzymaniak/Sportradar
cd Sportradar
```

### 3. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 4. Inicjalizacja bazy danych
```bash
python database.py   # Tworzy schemat
python load_data.py  # Wczytuje dane z data.json
```

### 5. Uruchomienie serwera
```bash
".\.venv\Scripts\python.exe" -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 6. Dostęp do aplikacji
Otwórz w przeglądarce:
```
http://localhost:8000/
```


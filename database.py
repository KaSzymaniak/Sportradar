import sqlite3
import os
from pathlib import Path


DB_PATH = Path(__file__).parent / "sports_calendar.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Stworzenie tabeli ligi/turnieje
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE
        )
    ''')
    
    # 2. Stworzenie tabeli etapów turnieju
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ordering INTEGER,
            _competition_id INTEGER NOT NULL,
            FOREIGN KEY (_competition_id) REFERENCES competitions(id)
        )
    ''')
    
    # 3. Stworzenie tabeli drużyn
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            official_name TEXT,
            abbreviation TEXT,
            country_code TEXT
        )
    ''')
    
    # 4. Stworzenie tabeli meczów
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER,
            date_venue DATE NOT NULL,
            time_venue_utc TIME,
            stadium TEXT,
            status TEXT,
            home_goals INTEGER,
            away_goals INTEGER,
            winner TEXT,
            _home_team_id INTEGER,
            _away_team_id INTEGER,
            _stage_id INTEGER NOT NULL,
            _competition_id INTEGER NOT NULL,
            FOREIGN KEY (_home_team_id) REFERENCES teams(id),
            FOREIGN KEY (_away_team_id) REFERENCES teams(id),
            FOREIGN KEY (_stage_id) REFERENCES stages(id),
            FOREIGN KEY (_competition_id) REFERENCES competitions(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")

if __name__ == "__main__":
    init_db()

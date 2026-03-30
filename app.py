from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from pydantic import BaseModel
import os

# Model dla dodawania nowego meczu
class EventInput(BaseModel):
    date_venue: str
    time_venue_utc: str
    home_team: str = None
    away_team: str = None
    home_goals: int = None
    away_goals: int = None
    status: str
    season: int

# Utwórz aplikację FastAPI
app = FastAPI(title="Sports Event Calendar")

# Endpoint: Pobierz wszystkie mecze
@app.get("/events")
def get_events():
    """Zwraca listę wszystkicheventow z informacją o drużynach"""
    conn = get_connection()
    c = conn.cursor()
    
    # Jedno zapytanie SQL 
    c.execute("""
        SELECT 
            e.id,
            e.season,
            e.date_venue,
            e.time_venue_utc,
            ht.name as home_team,
            at.name as away_team,
            e.home_goals,
            e.away_goals,
            e.status,
            comp.name as competition,
            s.name as stage
        FROM events e
        LEFT JOIN teams ht ON e._home_team_id = ht.id
        LEFT JOIN teams at ON e._away_team_id = at.id
        LEFT JOIN competitions comp ON e._competition_id = comp.id
        LEFT JOIN stages s ON e._stage_id = s.id
        ORDER BY e.date_venue DESC
    """)
    
    # Konwersja wyników na listę słowników
    events = []
    for row in c.fetchall():
        events.append({
            "id": row[0],
            "season": row[1],
            "date": row[2],
            "time": row[3],
            "home_team": row[4],
            "away_team": row[5],
            "home_goals": row[6],
            "away_goals": row[7],
            "status": row[8],
            "competition": row[9],
            "stage": row[10]
        })
    
    conn.close()
    return events


# Endpoint: Pobierz jeden mecz
@app.get("/events/{event_id}")
def get_event(event_id: int):
    """Zwraca szczegóły jednego meczu"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT 
            e.id,
            e.season,
            e.date_venue,
            e.time_venue_utc,
            ht.name as home_team,
            at.name as away_team,
            e.home_goals,
            e.away_goals,
            e.status,
            comp.name as competition,
            s.name as stage,
            e.stadium
        FROM events e
        LEFT JOIN teams ht ON e._home_team_id = ht.id
        LEFT JOIN teams at ON e._away_team_id = at.id
        LEFT JOIN competitions comp ON e._competition_id = comp.id
        LEFT JOIN stages s ON e._stage_id = s.id
        WHERE e.id = ?
    """, (event_id,))
    
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Mecz nie znaleziony")
    
    return {
        "id": row[0],
        "season": row[1],
        "date": row[2],
        "time": row[3],
        "home_team": row[4],
        "away_team": row[5],
        "home_goals": row[6],
        "away_goals": row[7],
        "status": row[8],
        "competition": row[9],
        "stage": row[10],
        "stadium": row[11]
    }


# Endpoint: Pobierz listę lig/turniejów
@app.get("/competitions")
def get_competitions():
    """Zwraca listę dostępnych lig"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT id, name, slug FROM competitions")
    
    competitions = []
    for row in c.fetchall():
        competitions.append({
            "id": row[0],
            "name": row[1],
            "slug": row[2]
        })
    
    conn.close()
    return competitions


# Strona główna - HTML
@app.get("/")
def get_home():
    """Zwraca stronę HTML"""
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(html_path)


# Endpoint: Dodaj nowy mecz
@app.post("/events")
def add_event(event: EventInput):
    """Dodaje nowy mecz do bazy danych"""
    conn = get_connection()
    c = conn.cursor()
    
    try:
        # Znajdz team_id dla druzyn
        home_team_id = None
        away_team_id = None
        
        if event.home_team:
            c.execute("SELECT id FROM teams WHERE name = ?", (event.home_team,))
            row = c.fetchone()
            home_team_id = row[0] if row else None
        
        if event.away_team:
            c.execute("SELECT id FROM teams WHERE name = ?", (event.away_team,))
            row = c.fetchone()
            away_team_id = row[0] if row else None
        
        # Jezeli mecz zaplanowany, wyniku nie moze miec wartosci
        if event.status == "scheduled":
            home_goals = None
            away_goals = None
        else:
            home_goals = event.home_goals
            away_goals = event.away_goals
        
        # Wstaw nowy mecz
        c.execute("""
            INSERT INTO events (
                season,
                date_venue,
                time_venue_utc,
                home_goals,
                away_goals,
                status,
                _competition_id,
                _stage_id,
                _home_team_id,
                _away_team_id
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                1,
                1,
                ?,
                ?
            )
        """, (
            event.season,
            event.date_venue,
            event.time_venue_utc,
            home_goals,
            away_goals,
            event.status,
            home_team_id,
            away_team_id
        ))
        
        conn.commit()
        
        # Pobierz nowo dodany mecz
        event_id = c.lastrowid
        c.execute("""
            SELECT 
                e.id,
                e.season,
                e.date_venue,
                e.time_venue_utc,
                ht.name as home_team,
                at.name as away_team,
                e.home_goals,
                e.away_goals,
                e.status,
                comp.name as competition,
                s.name as stage
            FROM events e
            LEFT JOIN teams ht ON e._home_team_id = ht.id
            LEFT JOIN teams at ON e._away_team_id = at.id
            LEFT JOIN competitions comp ON e._competition_id = comp.id
            LEFT JOIN stages s ON e._stage_id = s.id
            WHERE e.id = ?
        """, (event_id,))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "season": row[1],
                "date": row[2],
                "time": row[3],
                "home_team": row[4],
                "away_team": row[5],
                "home_goals": row[6],
                "away_goals": row[7],
                "status": row[8],
                "competition": row[9],
                "stage": row[10]
            }
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

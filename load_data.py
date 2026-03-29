import json
import os
from database import get_connection, init_db

json_path = os.path.join(os.path.dirname(__file__), "data.json")
with open(json_path) as f:
    data = json.load(f)

init_db()
conn = get_connection()
c = conn.cursor()

for e in data['data']:
    comp = e.get('originCompetitionName')
    c.execute('INSERT OR IGNORE INTO competitions (name, slug) VALUES ("' + str(comp) + '", "' + str(e.get('originCompetitionId')) + '")')
    cid = c.execute('SELECT id FROM competitions WHERE name = "' + str(comp) + '"').fetchone()[0]
    
    stage = e.get('stage', {})
    c.execute('INSERT OR IGNORE INTO stages (name, ordering, _competition_id) VALUES ("' + str(stage.get('name')) + '", ' + str(stage.get('ordering')) + ', ' + str(cid) + ')')
    sid = c.execute('SELECT id FROM stages WHERE name = "' + str(stage.get('name')) + '" AND _competition_id = ' + str(cid)).fetchone()[0]
    
    home = e.get('homeTeam')
    hid = None
    if home:
        c.execute('INSERT OR IGNORE INTO teams (name, official_name, abbreviation, country_code) VALUES ("' + str(home.get('name')) + '", "' + str(home.get('officialName')) + '", "' + str(home.get('abbreviation')) + '", "' + str(home.get('teamCountryCode')) + '")')
        hid = c.execute('SELECT id FROM teams WHERE name = "' + str(home.get('name')) + '"').fetchone()[0]
    
    away = e.get('awayTeam')
    aid = None
    if away:
        c.execute('INSERT OR IGNORE INTO teams (name, official_name, abbreviation, country_code) VALUES ("' + str(away.get('name')) + '", "' + str(away.get('officialName')) + '", "' + str(away.get('abbreviation')) + '", "' + str(away.get('teamCountryCode')) + '")')
        aid = c.execute('SELECT id FROM teams WHERE name = "' + str(away.get('name')) + '"').fetchone()[0]
    
    res = e.get('result') or {}
    c.execute('INSERT INTO events (season, date_venue, time_venue_utc, stadium, status, home_goals, away_goals, winner, _home_team_id, _away_team_id, _stage_id, _competition_id) VALUES (' + str(e.get('season')) + ', "' + str(e.get('dateVenue')) + '", "' + str(e.get('timeVenueUTC')) + '", ' + ('NULL' if e.get('stadium') is None else '"' + str(e.get('stadium')) + '"') + ', "' + str(e.get('status')) + '", ' + ('NULL' if res.get('homeGoals') is None else str(res.get('homeGoals'))) + ', ' + ('NULL' if res.get('awayGoals') is None else str(res.get('awayGoals'))) + ', ' + ('NULL' if res.get('winner') is None else '"' + str(res.get('winner')) + '"') + ', ' + ('NULL' if hid is None else str(hid)) + ', ' + ('NULL' if aid is None else str(aid)) + ', ' + str(sid) + ', ' + str(cid) + ')')

conn.commit()
conn.close()

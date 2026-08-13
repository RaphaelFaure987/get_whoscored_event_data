import soccerdata as sd
import logging
from pathlib import Path

logging.basicConfig(filename="scrape.log", level=logging.INFO)

LEAGUES = [
    #"GER-Bundesliga",
    #"ITA-Serie A",
    "ENG-Premier League"
]
SEASONS = [f"{y}-{y+1}" for y in range(2023, 2024)]  

failed_matches = []

for league in LEAGUES:
    for season in SEASONS:
        try:
            ws = sd.WhoScored(
                leagues=league, 
                seasons=season,
                headless=False,   # You can change it but you'll probably get blocked very fast
            )
            schedule = ws.read_schedule(force_cache=True)
        except Exception as e:
            logging.error(f"Calendrier introuvable {league} {season}: {e}")
            continue
        
        for match_id in schedule["game_id"]:
            try:
                # raw whoscored with qualifiers
                events_raw = ws.read_events(match_id=match_id, output_fmt="raw",retry_missing=True,on_error="skip")

                ws.read_events(
                    match_id=match_id,
                    output_fmt="spadl",
                    retry_missing=True,
                    on_error="skip",   # ne bloque pas tout le run
                )
                logging.info(f"OK {league} {season} match {match_id}")
            except Exception as e:
                logging.warning(f"Échec {league} {season} {match_id}: {e}")
                failed_matches.append((league, season, match_id))

# à la fin : relancer uniquement failed_matches, avec un délai plus long "ENG-Premier League",
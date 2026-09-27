import requests
import os
import pandas
from dotenv import load_dotenv

BASE_URL = "https://v3.football.api-sports.io"

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

headers = {
    'x-apisports-key': API_KEY
}

def get_and_save_games(league_id, season):
    url = f"{BASE_URL}/fixtures?league={league_id}&season={season}&status=FT"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return

    games = response.json().get("response", [])
    games_list = []

    for game in games:
        fixture = game.get("fixture", {})
        game_date = fixture.get("date", "")[:10]
        round = game.get("league", {}).get("round", "")

        teams = game.get("teams", {})
        home_id = teams.get("home", {}).get("id")
        home_name = teams.get("home", {}).get("name")
        away_id = teams.get("away", {}).get("id")
        away_name = teams.get("away", {}).get("name")

        goals = game.get("goals", {})
        home_goals = goals.get("home")
        away_goals = goals.get("away")

        if home_goals is None or away_goals is None:
            continue

        if home_goals > away_goals:
            result = 1
        elif home_goals == away_goals:
            result = 0
        else:
            result = 2

        games_list.append({
            "date": game_date,
            "round": round,
            "home_id": home_id,
            "home_name": home_name,
            "away_id": away_id,
            "away_name": away_name,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "result": result
        })

        df = pandas.DataFrame(games_list)

        filename = "gamehistory_v2.csv"
        df.to_csv(filename, index=False, encoding='utf-8')

if __name__ == "__main__":
    get_and_save_games(39, 2023)
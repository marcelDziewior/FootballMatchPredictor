import requests
import os
import pandas
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "X-Auth-Token": API_KEY
}

BASE_URL = "https://api.football-data.org/v4"

def download_league_table(league_id):
    url = f"{BASE_URL}/competitions/{league_id}/standings"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()

        print(f"Tabela: {data['competition']['name']}")
        tabela = data["standings"][0]["table"]

        for team in tabela[:10]:
            pos = team["position"]
            name = team["team"]["name"]
            points = team["points"]
            games = team["playedGames"]
            form = team.get("form")
            print(f"{pos}. {name} - {points} pts. for {games} games played. {form}")
    elif response.status_code == 403:
        print("Invalid token")
    else:
        print(f"{response.status_code} - {response.text}")

def get_and_save_games(league_id):
    url = f"{BASE_URL}/competitions/{league_id}/matches?status=FINISHED"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return

    games = response.json().get("matches", [])
    games_list = []

    for game in games:
        home_id = game.get("homeTeam", {}).get("id")
        home_name = game.get("homeTeam", {}).get("name")
        away_id = game.get("awayTeam", {}).get("id")
        away_name = game.get("awayTeam", {}).get("name")

        score_data = game.get("score", {}).get("fullTime", {})
        if score_data is None:
            score_data = {}

        goals_home = score_data.get("home")
        goals_away = score_data.get("away")

        if goals_home is None or goals_away is None:
            continue


        #1 = home team win, 0 = tie, 2 = away team win
        if goals_home > goals_away:
            result = 1
        elif goals_home == goals_away:
            result = 0
        else:
            result = 2

        games_list.append({
            "date": game.get("utcDate")[:10],
            "matchday": game.get("matchday"),
            "homeID": home_id,
            "homeTeam": home_name,
            "awayID": away_id,
            "awayTeam": away_name,
            "goalsHome": goals_home,
            "goalsAway": goals_away,
            "result": result
        })

        df = pandas.DataFrame(games_list)

        filename = "gamehistory.csv"
        df.to_csv(filename, index=False, encoding='utf-8')


if __name__ == "__main__":
    #download_league_table("PL")
    get_and_save_games("PL")
import pandas as pd

df = pd.read_csv("gamehistory.csv")
df = df.sort_values(by="data").reset_index(drop=True)

teams_history = {}

form_home_points = []
form_away_points = []
form_home_goals = []
form_away_goals = []

def avg(history, key):
    if len(history) == 0:
        return 0.0

    summ = sum(game[key] for game in history)
    return round(summ / len(history), 2)

for index, row in df.iterrows():
    home_id = row['homeID']
    away_id = row['awayID']

    if home_id not in teams_history: teams_history[home_id] = []
    if away_id not in teams_history: teams_history[away_id] = []

    home_history = teams_history[home_id][-5:]
    away_history = teams_history[away_id][-5:]
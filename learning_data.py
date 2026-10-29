import pandas as pd

# Importing data
df = pd.read_csv("gamehistory_v4.csv")

# Making sure that records are sorted by date
df = df.sort_values(by="date").reset_index(drop=True)

teams_history = {}

form_home_points = []
form_away_points = []
form_home_goals = []
form_away_goals = []

def avg(history, key):
    if len(history) == 0:
        return 0.0
    return round(sum(match[key] for match in history) / len(history), 2)
print("Calculating history of last 5 games...")

for index, row in df.iterrows():
    home_id = row['homeID']
    away_id = row['awayID']

    if home_id not in teams_history: teams_history[home_id] = []
    if away_id not in teams_history: teams_history[away_id] = []

    home_history = teams_history[home_id][-5:]
    away_history = teams_history[away_id][-5:]

    form_home_points.append(avg(home_history, 'points'))
    form_away_points.append(avg(away_history, 'points'))
    form_home_goals.append(avg(home_history, 'goalsScored'))
    form_away_goals.append(avg(away_history, 'goalsScored'))

    home_goals = row['goalsHome']
    away_goals = row['goalsAway']
    result = row['result']

    pts_home = 3 if result == 1 else (1 if result == 0 else 0)
    pts_away = 3 if result == 2 else (1 if result == 0 else 0)

    teams_history[home_id].append({'goalsScored': home_goals, 'points': pts_home})
    teams_history[away_id].append({'goalsScored': away_goals, 'points': pts_away})

df['home_avg_pts_5m'] = form_home_points
df['away_avg_pts_5m'] = form_away_points
df['home_avg_goals_5m'] = form_home_goals
df['away_avg_goals_5m'] = form_away_goals

df = df[df['matchday'] > 2].reset_index(drop=True)

end_file_name = "data_ready_for_training_second_api.csv"
df.to_csv(end_file_name, index=False, encoding='utf-8')

print("Success")
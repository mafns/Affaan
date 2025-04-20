import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Fetch match data from Football-Data.org API (v4)
def fetch_epl_data(season):
    url = f"https://api.football-data.org/v4/competitions/PL/matches?season={season}"
    headers = {'X-Auth-Token': '346bbb1109cc441ab1a9684ef420a2d9'}  # Replace with your API token

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print("Response content:", response.text)
            return None

        matches = []
        for match in response.json()['matches']:
            if match['status'] == 'FINISHED':
                matches.append({
                    'home_team': match['homeTeam']['name'],
                    'away_team': match['awayTeam']['name'],
                    'home_goals': match['score']['fullTime']['home'],
                    'away_goals': match['score']['fullTime']['away'],
                    'result': match['score']['winner']
                })

        df = pd.DataFrame(matches)
        print(f"\nEPL {season} Match Data Sample:")
        print(df.head())
        return df

    except Exception as e:
        print(f"Error fetching football data: {e}")
        return None

# Feature engineering: team form
def prepare_features(df):
    teams = pd.unique(df[['home_team', 'away_team']].values.ravel())
    form = {team: [] for team in teams}

    for idx, row in df.iterrows():
        home_form = np.mean(form[row['home_team']][-5:]) if form[row['home_team']] else 0.5
        away_form = np.mean(form[row['away_team']][-5:]) if form[row['away_team']] else 0.5

        df.loc[idx, 'home_form'] = home_form
        df.loc[idx, 'away_form'] = away_form

        result = 1 if row['result'] == 'HOME_TEAM' else (0 if row['result'] == 'AWAY_TEAM' else 0.5)
        form[row['home_team']].append(result)
        form[row['away_team']].append(1 - result)

    return df.dropna()

# Train model
def train_model(df):
    X = df[['home_form', 'away_form']]
    y = df['result'].map({'HOME_TEAM': 1, 'DRAW': 0, 'AWAY_TEAM': 2})

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\nModel Accuracy: {acc:.2%}")
    return model

# Predict upcoming matches
def predict_fixtures(model, fixtures):
    print("\nUpcoming Match Predictions:")
    print("=" * 50)
    print(f"{'Home':<25}{'Away':<25}{'Prediction':<15}")
    print("-" * 50)

    for idx, match in fixtures.iterrows():
        features = pd.DataFrame([[match['home_form'], match['away_form']]],
                                columns=['home_form', 'away_form'])
        pred = model.predict(features)[0]
        outcome = "Home Win" if pred == 1 else ("Draw" if pred == 0 else "Away Win")
        print(f"{match['home_team']:<25}{match['away_team']:<25}{outcome:<15}")

if __name__ == "__main__":
    print("Premier League Match Predictor")

    # Step 1: Load historical match data
    data = fetch_epl_data(2023)

    if data is not None:
        # Step 2: Prepare features
        prepared_data = prepare_features(data)

        # Step 3: Train the model
        trained_model = train_model(prepared_data)

        # Step 4: Upcoming fixtures with form values
        upcoming = pd.DataFrame([
            {'home_team': 'Arsenal', 'away_team': 'Chelsea', 'home_form': 0.8, 'away_form': 0.4},
            {'home_team': 'Man United', 'away_team': 'Liverpool', 'home_form': 0.6, 'away_form': 0.7},
            {'home_team': 'Tottenham', 'away_team': 'Newcastle United', 'home_form': 0.5, 'away_form': 0.6},
            {'home_team': 'Brighton & Hove Albion', 'away_team': 'Brentford', 'home_form': 0.7, 'away_form': 0.5},
            {'home_team': 'Aston Villa', 'away_team': 'Man City', 'home_form': 0.6, 'away_form': 0.9},
            {'home_team': 'West Ham United', 'away_team': 'Everton', 'home_form': 0.4, 'away_form': 0.3},
            {'home_team': 'Wolves', 'away_team': 'Burnley', 'home_form': 0.5, 'away_form': 0.2},
            {'home_team': 'Fulham', 'away_team': 'Nottingham Forest', 'home_form': 0.3, 'away_form': 0.4},
        ])

        # Step 5: Make predictions
        predict_fixtures(trained_model, upcoming)


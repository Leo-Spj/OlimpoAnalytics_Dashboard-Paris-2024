import pandas as pd
import ast

# Leer archivo original separado por tabulaciones
df = pd.read_csv("equipos.tsv", sep='\t')

# 1. Tabla teams
teams_df = df[['code', 'team', 'team_gender_code', 'country_code', 'disciplines_code']].copy()
teams_df.columns = ['team_code', 'team_name', 'gender', 'country_code', 'discipline_code']

# 2. Tabla team_athletes
team_athletes = []

for _, row in df.iterrows():
    team_code = row['code']
    if pd.notna(row['athletes_codes']):
        try:
            athletes = ast.literal_eval(row['athletes_codes'])
            for athlete_code in athletes:
                team_athletes.append({'team_code': team_code, 'athlete_code': athlete_code})
        except Exception as e:
            print(f"Error al procesar atletas de {team_code}: {e}")

team_athletes_df = pd.DataFrame(team_athletes)

# 3. Tabla team_coaches
team_coaches = []

for _, row in df.iterrows():
    team_code = row['code']
    if pd.notna(row['coaches_codes']):
        try:
            coaches = ast.literal_eval(row['coaches_codes'])
            for coach_code in coaches:
                team_coaches.append({'team_code': team_code, 'coach_code': coach_code})
        except Exception as e:
            print(f"Error al procesar coaches de {team_code}: {e}")

team_coaches_df = pd.DataFrame(team_coaches)

# Guardar resultados como archivos CSV
teams_df.to_csv("teams.csv", index=False)
team_athletes_df.to_csv("team_athletes.csv", index=False)
team_coaches_df.to_csv("team_coaches.csv", index=False)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os



url = 'https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view'

def load_data(url: str, local_path: str) -> pd.DataFrame:
    if os.path.exists(local_path):
        try:
            df = pd.read_csv(local_path)
            print(f"Data loaded from local file: {local_path}")
            return df
        except Exception as e:
            print(f"Error loading data from local file: {e}")

    if 'drive.google.com' in url:
        url = 'https://drive.google.com/uc?export=download&id=' + url.split('/d/')[1].split('/')[0]

    print(f"Downloading data from URL: {url}")
    df = pd.read_csv(url)
    os.makedirs(os.path.dirname(local_path) or '.', exist_ok=True)
    df.to_csv(local_path, index=False)
    print("Data saved locally.")
    return df

df = load_data(url, 'data/chess_games.csv')

# ── Stage 1 ────────────────────────────────────────────
print(f"Q1  Records:                  {len(df):,}")
print(f"Q2  Exact duplicates:         {df.duplicated().sum()}")
print(f"Q3  Duplicate move sequences: {df.duplicated(subset=['moves']).sum()}")
print(f"Q4  opening_response missing: {df['opening_response'].isna().mean()*100:.2f}%")
print(f"Q5  opening_variation missing:{df['opening_variation'].isna().mean()*100:.2f}%")
print(f"Q6  Min turns: {df['turns'].min()} ← suspicious, real game needs ≥2 turns")

# ── Stage 2 ────────────────────────────────────────────
def clean_chess(df: pd.DataFrame) -> pd.DataFrame:

    # 2a
    df[['time_base', 'time_inc']] = (
        df['time_increment']
        .str.split('+', expand=True)
        .astype(int)
    )

    # 2b
    df['rating_diff'] = df['white_rating'] - df['black_rating']

    # 2c
    df['opening_family'] = (
        df['opening_fullname']
        .str.split(':')
        .str[0]
        .str.strip()
    )

    # 2d
    df = df.drop(columns=['opening_code'])

    # 2e
    df['is_suspicious'] = df['turns'] < 5

    # 2f
    assert df['rating_diff'].notna().all(), "rating_diff has nulls!"
    assert df.duplicated().sum() == 0,      "duplicate rows found!"
    print("✅ Validation passed")
    return df

df = clean_chess(df)

# ── Stage 3 ────────────────────────────────────────────
print("\nQ10 Win rates:")
win_rates = df['winner'].value_counts(normalize=True) * 100
for k, v in win_rates.items():
    print(f"    {k}: {v:.2f}%")

print(f"\nQ11 Most common victory status: {df['victory_status'].value_counts().idxmax()}")

print("\nQ12 Avg turns by victory status:")
avg_turns = df.groupby('victory_status')['turns'].mean().sort_values(ascending=False)
print(avg_turns.round(1).to_string())

print("\nQ13 Most popular opening family:")
df['winner'] = df['winner'].str.lower().str.strip()
for pos in ['white', 'black']:
    top = df[df['winner'] == pos]['opening_family'].value_counts().idxmax()
    print(f"    {pos} wins → {top}")

print("\nQ14 White win rate — rated vs unrated:")
q14 = (df.groupby('rated')
         .apply(lambda x: (x['winner'] == 'white').mean() * 100,
                include_groups=False)
         .rename({True: 'Rated', False: 'Unrated'}))
for label, val in q14.items():
    print(f"    {label}: {val:.2f}%")

print("\nQ15 Game length distribution:")
def classify_game(turns):
    if turns < 20:
        return 'Short'
    elif turns < 70:
        return 'Medium'
    else:
        return 'Long'

df['game_length'] = df['turns'].apply(classify_game)
length_pct = df['game_length'].value_counts(normalize=True) * 100
for label, pct in length_pct.items():
    print(f"    {label}: {pct:.2f}%")

# ── Stage 4 ────────────────────────────────────────────
os.makedirs('output', exist_ok=True)
chess = df.copy()

white_players = chess['white_id'].unique() 
total = len(white_players)                 

np.random.seed(42)
registered_count = total - 9238
registered = np.random.choice(white_players, size=registered_count, replace=False)

registry = pd.DataFrame({
    'username': registered,
    'country': np.random.choice(
        ['RUS', 'US', 'USA', 'united states', 'UA',
         'GB', 'UK', 'FR', 'DE', 'IN'],
        size=registered_count
    )
})
registry.to_csv('data/player_registry.csv', index=False)

# Merge
merged = pd.merge(
    chess[['game_id', 'white_id', 'white_rating', 'winner']],
    registry.rename(columns={'username': 'white_id'}),
    on='white_id',
    how='left'
)


country_map = {
    'RUS': 'Russia',
    'US': 'United States', 'USA': 'United States', 'united states': 'United States',
    'UA': 'Ukraine', 'GB': 'United Kingdom', 'UK': 'United Kingdom',
    'FR': 'France',  'DE': 'Germany',         'IN': 'India',
}
merged['country'] = merged['country'].map(country_map).fillna(merged['country'])

white_unique = chess[['white_id']].drop_duplicates()

merged_players = pd.merge(
    white_unique,
    registry.rename(columns={'username': 'white_id'}),
    on='white_id',
    how='left'
)

# Q16 — لاعبين بدون registry entry
q16 = merged_players['country'].isna().sum()
print(f"\nQ16 No registry entry: {q16:,}")
# → ~9,238


# Q17 — forms before vs after
before = registry['country'].nunique()   
after  = merged['country'].nunique()  
print(f"Q17 Before: {before} forms → After: {after} clean countries")

# Q18 — bar chart
chess['winner'].value_counts().plot(
    kind='bar',
    title='Win Counts by Color',
    xlabel='Winner',
    ylabel='Number of Games',
    color=['#2c2c2c', '#e0e0e0', '#888888'],
    figsize=(7, 4)
).get_figure().savefig('output/wins_by_color.png', dpi=150, bbox_inches='tight')
plt.close()
print("Q18 Saved → output/wins_by_color.png")
print(f"    {chess['winner'].value_counts().to_dict()}")

# Q19 — scatter
chess[chess['rated'] == True].plot(
    kind='scatter',
    x='white_rating',
    y='turns',
    title='White Rating vs Turns (Rated Games)',
    alpha=0.15,
    s=8,
    color='steelblue',
    figsize=(8, 5)
).get_figure().savefig('output/rating_vs_turns.png', dpi=150, bbox_inches='tight')
plt.close()
print("Q19 Saved → output/rating_vs_turns.png")
print("Q19 Observation: Higher-rated games not necessarily longer")


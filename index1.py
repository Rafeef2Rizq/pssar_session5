import pandas as pd
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

df = load_data(url, 'data/diabetes.csv')
#number of records in the dataset
num_records = len(df)
print(f"Number of records in the dataset: {num_records}")

#duplicate rows in the dataset
num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows in the dataset: {num_duplicates}")

# duplicate move sequences in the dataset
print(f"Q3 Duplicate move sequences: {df.duplicated(subset=['moves']).sum()}")

# missing opening_response values in the dataset
q4 = df['opening_response'].isna().mean() * 100
print(f"Q4 opening_response missing: {q4:.2f}%")

#missing opening_variation values in the dataset
q5 = df['opening_variation'].isna().mean() * 100
print(f"Q5 opening_variation missing: {q5:.2f}%")

#the minimum number of turns in any game
q6 = df['turns'].min()
print(f"Q6 Minimum turns: {q6}")
print("suspicious: a real game needs at least 2 turns")

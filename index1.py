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
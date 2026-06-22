import pandas as pd

def load_data():
    data = pd.read_csv('../Data/Hyderbad_House_price.csv')
    return data
import pandas as pd

def createDF(filename):
    df = pd.read_json(filename)
    return df

import pandas as pd


def get_number_of_built_flats():
    number_of_built_flats = pd.read_excel('data/built_flats.xlsx', index_col='kraj')
    return number_of_built_flats
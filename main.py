from sources.world_bank import get_countries, get_alcohol_consumption
from sources.google_sheets import auth, write_df
import os.path
import pandas as pd

SHEET_ID = '1tKdtPdbDPfQNmaBYv1l0SbUUEA_7rzt_BMAnHcJhHqo'

if __name__ == '__main__':
    service = auth()
    countries = get_countries()
    alcohol = get_alcohol_consumption()
    data = pd.merge(countries, alcohol, how='inner', on=['name'])

    # individual sources
    countries.to_csv(os.path.expanduser('data/countries.csv'))
    alcohol.to_csv(os.path.expanduser('data/alcohol.csv'))

    # combined
    data.to_csv(os.path.expanduser('data/data.csv'))
    data = data.dropna()
    write_df(service, SHEET_ID, 'A1', data)



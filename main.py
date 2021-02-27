from sources.world_bank import get_countries
from sources.google_sheets import auth, write_df
import os.path

SHEET_ID = '1tKdtPdbDPfQNmaBYv1l0SbUUEA_7rzt_BMAnHcJhHqo'

if __name__ == '__main__':
    countries = get_countries()
    countries.to_csv(os.path.expanduser('data/countries.csv'))

    service = auth()
    response = write_df(service, SHEET_ID, 'A1', countries)


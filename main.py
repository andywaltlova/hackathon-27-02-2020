from sources.world_bank import get_countries, get_alcohol_consumption
from sources.world_bank import get_cause_of_death_by_road_traffic_injury, \
    get_cause_of_death_by_injury
from sources.google_sheets import auth, write_df
import os.path
import pandas as pd

SHEET_ID = '1tKdtPdbDPfQNmaBYv1l0SbUUEA_7rzt_BMAnHcJhHqo'

if __name__ == '__main__':
    service = auth()
    countries = get_countries()
    alcohol = get_alcohol_consumption()
    injuries = get_cause_of_death_by_injury()
    rtraffic_injuries = get_cause_of_death_by_road_traffic_injury()

    data = pd.merge(countries, alcohol, how='inner', on=['name'])
    data = pd.merge(data, injuries, how='inner', on=['name'])
    data = pd.merge(data, rtraffic_injuries, how='inner', on=['name'])

    # individual sources
    countries.to_csv(os.path.expanduser('data/countries.csv'))
    alcohol.to_csv(os.path.expanduser('data/alcohol.csv'))
    injuries.to_csv(os.path.expanduser('data/injuries.csv'))
    rtraffic_injuries.to_csv(os.path.expanduser('data/rtraffic_injuries.csv'))

    # combined
    data = data.dropna()
    data.to_csv(os.path.expanduser('data/data.csv'))
    write_df(service, SHEET_ID, 'A1', data)

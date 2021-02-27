from sources.google_sheets import auth, write_df
from sources.world_bank import get_countries, get_alcohol_consumption
from sources.world_bank import get_cause_of_death_by_road_traffic_injury
from sources.world_bank import get_cause_of_death_by_injury
from sources.hapiness_report import get_world_hapiness

import os.path
import pandas as pd

SHEET_ID = '1tKdtPdbDPfQNmaBYv1l0SbUUEA_7rzt_BMAnHcJhHqo'

if __name__ == '__main__':
    service = auth()

    # WorldBank sources
    countries = get_countries()
    alcohol = get_alcohol_consumption()
    injuries = get_cause_of_death_by_injury()
    rtraffic_injuries = get_cause_of_death_by_road_traffic_injury()
    countries.to_csv(os.path.expanduser('data/countries.csv'))
    alcohol.to_csv(os.path.expanduser('data/alcohol.csv'))
    injuries.to_csv(os.path.expanduser('data/injuries.csv'))
    rtraffic_injuries.to_csv(os.path.expanduser('data/rtraffic_injuries.csv'))

    # Kaggle
    hapiness = get_world_hapiness()

    # Combined
    data = pd.merge(countries, alcohol, how='left', on=['name'])
    data = pd.merge(data, injuries, how='left', on=['name'])
    data = pd.merge(data, rtraffic_injuries, how='left', on=['name'])
    data = pd.merge(data, hapiness, how='left', on=['name'])

    # data = data.dropna()
    data = data.fillna('')
    data.to_csv(os.path.expanduser('data/data.csv'))
    write_df(service, SHEET_ID, 'A1', data)

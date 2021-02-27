from sources.google_sheets import auth, write_df
from sources.world_bank import get_countries, get_alcohol_consumption
from sources.world_bank import get_cause_of_death_by_road_traffic_injury
from sources.world_bank import get_cause_of_death_by_injury
from sources.hapiness_report import get_world_hapiness
from sources.wikipedia_tables import get_legal_driking_age, get_driving_legal_limit
from sources.translations import create_complete_df

import os.path
import pandas as pd
from pandas.api.types import is_numeric_dtype


def fill_na_mean(df):
    for col in df.columns:
        if is_numeric_dtype(df[col].dtype):
            df[col] = df[col].fillna(df[col].mean())
    return df


SHEET_ID = '1tKdtPdbDPfQNmaBYv1l0SbUUEA_7rzt_BMAnHcJhHqo'
SHEET_ID_trans = '1KLoVcnGxeAfPP2z8s71VNx_g9h1Rv22rXdIxp-VQaos'

if __name__ == '__main__':
    service = auth()

    # WorldBank sources
    countries = get_countries()
    alcohol = get_alcohol_consumption()
    injuries = get_cause_of_death_by_injury()
    rtraffic_injuries = get_cause_of_death_by_road_traffic_injury()
    drinking_age = get_legal_driking_age()
    driving_limit = get_driving_legal_limit()

    # Kaggle
    hapiness = get_world_hapiness()

    # Google translation api
    #translation_df = create_complete_df()

    # Combined
    data = pd.merge(countries, alcohol, how='left', on=['name'])
    data = pd.merge(data, injuries, how='left', on=['name'])
    data = pd.merge(data, rtraffic_injuries, how='left', on=['name'])
    data = pd.merge(data, hapiness, how='left', on=['name'])
    data = pd.merge(data, drinking_age, how='left', on=['name'])
    data = pd.merge(data, driving_limit, how='left', on=['name'])

    data = fill_na_mean(data)
    data = data.fillna('')
    print(data.head())

    data.to_csv(os.path.expanduser('data/data.csv'))

    write_df(service, SHEET_ID, 'A1', data)
    # write_df(service, SHEET_ID_trans, 'A1', translation_df)

import pandas as pd
import os.path


def get_world_hapiness():
    path = os.path.expanduser('data/world_happines_report.csv')
    data = pd.read_csv(path)
    data = data.drop('Overall rank', axis=1)
    data = data.rename(columns={'Country or region': 'name',
                                'Score': 'Hapiness score'})
    return data

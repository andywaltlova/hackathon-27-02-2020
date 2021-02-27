import wikipedia as wp
import pandas as pd
import os.path
import re


def get_legal_driking_age():
    html = wp.page("Legal_drinking_age").html()
    df = pd.read_html(html)[3]

    df.columns = ['name', 'Administrative division', 'drinking age private',
                  'drinking age private', 'purchase age on-premise',
                  'purchase age off-premise', 'notes']
    df = df.iloc[:, [0, 1, 4, 5, 6]]

    df['purchase age on-premise'] = [re.sub('\[(.*)\]', '', x) for x in
                                     df['purchase age on-premise']]
    df['purchase age off-premise'] = [re.sub('\[(.*)\]', '', x) for x in
                                      df['purchase age off-premise']]

    df['Administrative division'] = df['Administrative division'].replace(
        'Switzerland (federal law)',
        'Switzerland')
    df['Administrative division'] = df['Administrative division'].replace(
        'United Kingdom',
        'United Kingdom general')

    df['Administrative division'] = df['Administrative division'].replace(
        'Czechia',
        'Czech Republic')
    df['name'] = df['name'].replace('Czechia',
                                    'Czech Republic')
    df['Administrative division'] = df['Administrative division'].replace(
        'Slovakia',
        'Slovak Republic')
    df['name'] = df['name'].replace('Slovakia',
                                    'Slovak Republic')
    df = df[(df['name'] == df['Administrative division']) | (
            df['Administrative division'] == 'England Wales')]
    df['notes'] = df['notes'].fillna('')
    df = df.drop('Administrative division', axis=1)
    df.to_csv(os.path.expanduser('data/drinking_age.csv'))
    return df


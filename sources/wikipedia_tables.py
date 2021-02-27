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

    names = ['purchase age on-premise', 'purchase age off-premise']
    for name in names:
        df[name] = [re.sub('\[(.*)\]', '', x).split(' ')[0].split('(')[0] for x
                    in df['purchase age on-premise']]

    df['notes'] = df['notes'].fillna('')
    df['notes'] = [re.sub('\[(.*)\]', '', x) for x in df['notes']]

    col_name = 'Administrative division'
    to_replace = {
        'Switzerland (federal law)': 'Switzerland',
        'United Kingdom': 'United Kingdom general',
        'Czechia': 'Czech Republic',
        'Slovakia': 'Slovak Republic'
    }
    for old, new in to_replace.items():
        df[col_name] = df[col_name].replace(old, new)

    df['name'] = df['name'].replace('Czechia', 'Czech Republic')
    df['name'] = df['name'].replace('Slovakia', 'Slovak Republic')

    df = df[(df['name'] == df['Administrative division']) | (
            df['Administrative division'] == 'England Wales')]

    df = df.drop('Administrative division', axis=1)
    df.to_csv(os.path.expanduser('data/drinking_age.csv'))
    return df


def get_driving_legal_limit():
    with open(os.path.expanduser('data\driving_limits.txt')) as f:
        lines = [re.sub('\[(.*)\]', '', l.strip()) for l in f.readlines()]
        countries = [l.split(': ')[0] for l in lines]
        limits = [l.split(': ')[1] if len(l.split(': ')) > 1 else '' for l in
                  lines]

    res = pd.DataFrame({'name': countries, 'Drunk driving limit': limits})
    return res

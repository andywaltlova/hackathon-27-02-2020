import wbdata
import pandas as pd
from datetime import datetime


def _flatten_column(inpt_dict, column):
    pref = column + '_'
    for k, v in inpt_dict[column].items():
        inpt_dict[pref + k] = v
    inpt_dict.pop(column)


def get_countries():
    countries = list(wbdata.get_country())
    for country in countries:
        nested_columns = ['region', 'adminregion', 'incomeLevel', 'lendingType']
        for nest_dict in nested_columns:
            _flatten_column(country, nest_dict)

    countries = pd.DataFrame(countries)
    countries = countries[['id', 'iso2Code', 'name', 'capitalCity']]

    wanted_countries = ['AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'JG', 'HR',
                        'CY', 'CZ', 'DK', 'EE', 'FO', 'FI', 'FR', 'DE', 'GI',
                        'GR', 'HU', 'IS', 'IE', 'IM', 'IT', 'XK', 'LV', 'LI',
                        'LT', 'LU', 'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL',
                        'PT', 'RO', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH',
                        'TR', 'UA', 'GB']
    countries = countries[(countries['iso2Code'].isin(wanted_countries))]
    return countries


def get_alcohol_consumption():
    m_name = 'Total alcohol consumption per capita, male (liters of pure ' \
             'alcohol, projected estimates, male 15+ years of age) '
    f_name = 'Total alcohol consumption per capita, female (liters of pure ' \
             'alcohol, projected estimates, male 15+ years of age) '

    year = datetime.strptime('2018', '%Y')
    f_data = wbdata.get_dataframe({'SH.ALC.PCAP.FE.LI': f_name}, data_date=year)
    m_data = wbdata.get_dataframe({'SH.ALC.PCAP.MA.LI': m_name}, data_date=year)

    data = pd.merge(f_data, m_data, how='left', on=['country'])
    data['name'] = data.index
    return data

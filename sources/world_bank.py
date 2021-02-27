import wbdata
import pandas as pd


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

# data = wbdata.get_dataframe({'SE.ADT.LITR.ZS':'Literacy'}, convert_date=True)
# print(data.head())

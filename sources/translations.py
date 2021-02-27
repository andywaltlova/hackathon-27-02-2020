import json
from googletrans import Translator
import pandas as pd


def create_country_language_df():
    countries_iso = {'AL': 'sq', 
                    'AD': 'ca', 
                    'AT': 'de', 
                    'BE': 'fr', 
                    'BG': 'bg',
                    'BA': 'bs',
                    'BY': 'be',
                    'CH': 'de',
                    'CY': 'el',
                    'CZ': 'cs',
                    'DE': 'de',
                    'DK': 'da',
                    'ES': 'es',
                    'EE': 'et',
                    'FI': 'fi',
                    'FR': 'fr',
                    'GB': 'en',
                    'GR': 'el',
                    'HR': 'hr',
                    'HU': 'hu',
                    'IE': 'ga',
                    'IS': 'is',
                    'IT': 'it',
                    'LT': 'lt',
                    'LU': 'lb',
                    'LV': 'lv',
                    'MD': 'ro',
                    'MK': 'mk',
                    'ME': 'hr',
                    'NL': 'nl',
                    'NO': 'no',
                    'PL': 'pl',
                    'PT': 'pt',
                    'RO': 'ro',
                    'RS': 'sr',
                    'SK': 'sk',
                    'SI': 'sl',
                    'SE': 'sv',
                    'TR': 'tr',
                    'UA': 'uk',
                    }
    lan_abbreviation = list(countries_iso.values())
    countries = list(countries_iso.keys())
    iso_lan_df = pd.DataFrame({'country_iso':countries, 'language': lan_abbreviation})
    return iso_lan_df


def get_translations_df():
    languages_all = ['sq', 'ca', 'de', 'fr', 'bg','bs','be','de','el','cs','de','da','es','et','fi','fr', 'en','el','hr','hu','ga', 'is','it','lt','lb','lv','ro','mk','hr','nl','no','pl','pt','ro','sr','sk','sl','sv','tr','uk']
    languages = list(set(languages_all))

    translator = Translator()
    
    sentence_to_translate = ['Dobrý večer.', 'Kde je tady nejbližší hospoda?', 'Točí tam pivo?', 'Jedno pivo, prosím.', 'Hospodský, ještě jedno.']
    
    language_df = []
    origin_texts = []
    translated = []

    for language in languages:
        for i in range(len(sentence_to_translate)):
            translated_sentence = translator.translate(sentence_to_translate[i], dest=language)
            language_df += [language]
            origin_texts += [sentence_to_translate[i]]
            translated += [translated_sentence.text]

    trans_df = pd.DataFrame({'language':language_df, 'origin': origin_texts, 'translated':translated})
    return trans_df


def create_complete_df():
    iso_lan_df = create_country_language_df()
    trans_df = get_translations_df()
    df_complete = pd.merge(iso_lan_df, trans_df, on=['language'])
    return df_complete


# print(create_complete_df())
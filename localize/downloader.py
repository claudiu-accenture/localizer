#!/usr/bin/env python3
import requests
import json
from .localization import Localization



class Downloader:

    def __init__(self):
        self._strip_keys = [
            'comments', 'note', 'view'
        ]

    def retrieve_localizations(self, config):
        urls = config.source_urls
        localizations = []
        print("Retrieving localizations:")
        for url in urls:
            print(' ', config.name_for_url(url), end='')
            text = self._download_localizations(url)
            parse_f = _parse_google_spreadsheets
            localizations += self._parse_localizations(text, parse_f)
            print("... done")

        print("Localizations acquired.\n")
        
        return localizations

    def _download_localizations(self, url):
        response = requests.get(url)
        if response.status_code not in range(200, 300):
            raise Exception("Could not download localization: {}".format(url))

        return response.text

    def _parse_localizations(self, raw, parser):
        raw_localizations = parser(raw)
        localizations = []
        for raw_loc in raw_localizations:
            localizations += [self._emit_localization(raw_loc)]

        return localizations

    def _emit_localization(self, raw):
        for key in self._strip_keys:
            if raw[key] is not None:
                del raw[key]

        loc_key = raw['stringname']
        del raw['stringname']

        loc_name = raw['name']
        del raw['name']

        loc_type = raw['type']
        del raw['type']

        # at this point, only languages remain
        lang_data = raw

        return Localization(loc_key, loc_name, lang_data, loc_type)





#===------------------------------------------------------------------------===#
# Cleanup Google Spreadsheets localizations

def _parse_google_spreadsheets(raw_json):
    try:
        raw_data = json.loads(raw_json)
    except:
        msg = "Failed to load the localization data JSON"
        hint = "check that the spreadsheet is public"
        raise Exception("{} (hint: {})".format(msg, hint))

    loc_data = raw_data['feed']['entry']
    if len(loc_data) == 0: 
        return []

    def clean(entry):
        removable_keys = [
            'category', 'content', 'id', 'link', 'title', 'updated'
        ]
        for key in removable_keys:
            if entry[key]:
                del entry[key]

        return entry

    def flatten(raw_entry):
        entry = {}
        for (key, value) in raw_entry.items():
            if key.startswith('gsx$'):
                key = key.replace('gsx$', '')
            if value['$t'] is not None:
                value = value['$t']

            entry[key] = value

        return entry


    data = []
    for entry in loc_data:
        data += [flatten(clean(entry))]

    return data
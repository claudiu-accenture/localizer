#!/usr/bin/env python3



class Localization:

    key = None
    name = None
    loc_type = None
    language_data = {}

    def __init__(self, key, name, language_data, loc_type):
        self.key = key
        self.name = name
        self.loc_type = loc_type

        self.language_data = {}
        for (lang, loc) in language_data.items():
            self.language_data[lang.capitalize()] = loc
            
    def __getitem__(self, key):
        return self.language_data[key]

    def __contains__(self, key):
        return key in self.language_data

    def __repr__(self):
        localizations = []
        for (lang, loc) in self.language_data.items():
            localizations += ['  {} => {}'.format(lang, loc)]

        return '\n'.join([
            "'{}': {}".format(self.key, self.loc_type),
        ] + localizations)



class iOSLocalization(Localization):

    def __init__(self, loc):
        loc_name = None
        if loc.loc_type == 'item':
            loc_name_parts = loc.name.split('-')
            if len(loc_name_parts) == 2:
                loc_name = loc_name_parts[1]
        else:
            loc_name = loc.name

        super().__init__(loc.key, loc_name, loc.language_data, loc.loc_type)



class AndroidLocalization(Localization):

    def __init__(self, loc):
        locs = None
        if type(loc) is list:
            locs = loc
            loc = loc[0]

        if loc.loc_type == 'item':
            loc_key = loc.name.split('-')[0]
        else:
            loc_key = loc.key

        super().__init__(loc_key, loc.name, loc.language_data, loc.loc_type)

        if locs:
            self._parse_string_array(locs)

    def _parse_string_array(self, locs):
        def parse_item(loc):
            loc.name = loc.name.split('-')[0]
            return loc

        lang_data = {}
        for lang in self.language_data.keys():
            lang_data[lang] = list(map(lambda loc: loc[lang], locs))

        self.language_data = lang_data




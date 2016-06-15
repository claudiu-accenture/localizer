#!/usr/bin/env python3
import yaml



class Config:

    default_language = None
    languages = []
    language_map = {}
    sources = {}

    def __init__(self, file_name):
        self._parse_config(file_name)


    def _parse_config(self, file_name):
        """Parse YAML config from `file_name`.

        The file should contain 3 things:
            - a language map, mapping the sheet columns with localizations
            - which default language
            - a list of {name, url} dictionaries to retrieve localizations
        """
        with open(file_name) as f:
            config = yaml.load(f)

        if config['languages']:
            self._parse_languages(config['languages'])

        if config['sources']:
            self.sources = config['sources']

        if config['default-language']:
            self.default_language = config['default-language']


    def _parse_languages(self, language_config):
        for language in language_config:
            language_name = list(language.keys())[0].strip()
            identifier = list(language.values())[0].strip()
            self.language_map[identifier] = language_name
            self.languages += [language_name]


    def __repr__(self):
        languages_map = []
        for lang, id in self.language_map.items():
            languages_map += ["  {} => {}".format(lang, id)]

        sources = []
        for source in self.sources:
            sources += ["  {} \n    => {}".format(source['name'], source['url'])]
        return '\n'.join([
            "Localization config",
            "-------------------",
            "Languages:        {}".format('  '.join(self.languages)),
            "Default language: {}".format(self.default_language),
            "Language map:",
            '\n'.join(languages_map),
            "Sources:",
            '\n'.join(sources),
            "-------------------",
        ])

    
    @property
    def source_urls(self):
        return list(map(lambda src: src['url'], self.sources))

    def name_for_url(self, query_url):
        for source in self.sources:
            if source['url'] == query_url:
                return source['name']

        return None
        

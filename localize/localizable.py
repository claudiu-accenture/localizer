#!/usr/bin/env python3
from pathlib import Path


class Localizable:

    def __init__(self, file_path, config):
        self.file_path = file_path
        self._config = config
        self.language = self._parse_language(file_path)

    @property
    def file_name(self):
        return Path(self.file_path).name

    def _parse_language(self, file_path):
        raise NotImplementedError

    def __repr__(self):
        return '\n'.join([
            "Language: {}".format(self.language),
            "Path: {}".format(self.file_path)
        ])


class iOSLocalizable(Localizable):

    def _parse_language(self, file_path):
        parent_stem = Path(file_path).parent.stem
        language_id = parent_stem.replace('.lproj', '')
        return self._config.language_map[language_id]


class AndroidLocalizable(Localizable):

    def _parse_language(self, file_path):
        parent_stem = Path(file_path).parent.stem
        if '-' in parent_stem:
            replace_str = 'values-'
        else:
            replace_str = 'values'

        language_id = parent_stem.replace(replace_str, '') or self._config.default_language
        return self._config.language_map[language_id]

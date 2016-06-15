#!/usr/bin/env python3


class LocalizationParser:

    def __init__(self, data=None):
        if not data:
            raise ValueError("No localization data")

        if not type(data) is list:
            raise ValueError("Localization parser expected a list")

        self.localizations = self.parse(data)

    def parse(self, data):
        pass

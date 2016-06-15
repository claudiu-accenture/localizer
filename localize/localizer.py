#!/usr/bin/env python3
from .localizable_data import iOSLocalizableData, AndroidLocalizableData
import re
import xml.etree.ElementTree as ET



class Localizer:

    _localizable_data = []
    _localization_map = {}
    
    def __init__(self, localization_map = None):
        self._localization_map = localization_map

    def parse(self, localizable):
        self.localizable_data = []
        self._parse_localizable(localizable)

    def localize(self, localizable):
        self._localizable = localizable
        self.localizable_data = []

        if not self._localization_map:
            raise ValueError("No localizations available")

        self._localize(localizable)



#===------------------------------------------------------------------------===#
# iOS localizer

class iOSLocalizer(Localizer):

    _replacement_key = None
    _localization_key = None

    _comment_key_pattern = r"(text|normalTitle|title|placeholder|segmentTitles\[\d+\]) \= \"(.+?)\";"
    _comment_key_regex = re.compile(_comment_key_pattern)

    localizable_data = []

    _localizable = None


    def _parse_localizable(self, localizable):
        with open(localizable.file_path) as f:
            for line in f:
                self._parse_line(line)

    def _localize(self, localizable):
        contents = []
        with open(localizable.file_path) as f:
            contents = [line for line in f]

        with open(localizable.file_path, 'w') as f:
            for line in contents:
                f.write(self._parse_line(line, localize=True))

    def _parse_line(self, line, localize=False):
        match = re.search(self._comment_key_regex, line)
        if line.startswith('/*') and match and len(match.groups()) == 2:
            self._localization_key = match.group(2)
        elif ' = ' in line and self._localization_key:
            (left, right) = line.split('" = "')
            if left and right:
                # strip quotes
                self._replacement_key = right.rstrip('";\n')
        elif ' = ' in line and not line.startswith('/*'):
            (left, right) = line.split('" = "')
            if left and right:
                self._localization_key = left[1:]
                self._replacement_key = right.rstrip('";\n')

        localizable_data = self._emit_localizable_data()
        if localizable_data:
            self._localizable_data += [self._emit_localizable_data()]

        if localize:
            if localizable_data and self._localization_map:
                return self._localize_line(line, localizable_data)
            else:
                return line

    def _localize_line(self, line, loc_data):
        key = loc_data.localization_key
        lang = self._localizable.language

        if key not in self._localization_map:
            if re.match(r"\w+\.\w+\.\w+", key):
                print("  ! Warning: '{}' not localized to '{}'".format(key, lang))
            return line

        localization = self._localization_map[key]

        if lang not in localization:
            print("  ! Warning: '{}' localization for '{}' missing".format(lang, key))
            return line

        if localization:
            key = loc_data.replacement_key
            (left, right) = line.split('" = "')
            if len(key) > 0:
                right = right.replace(key, localization[lang])
            else:
                right = localization[lang] + right
            localized_line = '" = "'.join([left, right])
            return localized_line
        else:
            return line


    def _emit_localizable_data(self):
        if not self._localization_key or not self._replacement_key:
            return None

        data = iOSLocalizableData(self._localization_key, self._replacement_key)
        self._localization_key = None
        self._replacement_key = None

        return data

    @property
    def localization_source_map(self):
        loc_map = {}
        for data in self.localizable_data:
            loc_map[data.replacement_key] = data.localization_key

        return loc_map


#===------------------------------------------------------------------------===#
# Android localizer

def _android_escape(string):
    # escape the single quotes
    # and de-escape double-escaped single quotes
    # ... Yes.
    return string.replace("'", "\\'").replace("\\\\'", "\\'")


class AndroidLocalizer(Localizer):

    def _parse_localizable(self, localizable):
        xml = ET.parse(localizable.file_path)
        root = xml.getroot()

        for child in root:
            localizable = self._parse_node(child)
            self.localizable_data += [localizable]

    def _parse_node(self, node):
        name = node.attrib['name']

        if node.tag == 'string-array':
            localizable_type = 'array-{}'.format(len(node))
        else:
            localizable_type = None

        localizable_data = AndroidLocalizableData(name, localizable_type)
        return localizable_data

    def _localize_node(self, node, loc_data):
        key = loc_data.localization_key
        lang = self._localizable.language

        if key not in self._localization_map:
            print("  ! Warning: '{}' not localized to '{}'".format(
                key, lang))
            return

        localization = self._localization_map[key]

        if lang not in localization:
            print("  ! Warning: '{}' localization for '{}' missing".format(
                lang, key))
            return

        if loc_data.localizable_type.startswith('array'):
            locs = localization[lang]
            for i, subnode in enumerate(node):
                subnode.text = _android_escape(locs[i])
        else:
            node.text = _android_escape(localization[lang])

    def _localize(self, localizable):
        xml = ET.parse(localizable.file_path)
        root = xml.getroot()

        for child in root:
            data = self._parse_node(child)
            self._localize_node(child, data)

        xml.write(localizable.file_path)

    @property
    def localization_source_map(self):
        return self.localizable_data
    



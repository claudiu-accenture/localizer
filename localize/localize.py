#!/usr/bin/env python3
import yaml
import os
import requests
from pathlib import Path
from .downloader import Downloader, _parse_google_spreadsheets
from .localizable import iOSLocalizable, AndroidLocalizable
from .localization import iOSLocalization, AndroidLocalization
from .localizer import iOSLocalizer, AndroidLocalizer



#===------------------------------------------------------------------------===#
# Common

def get_localizations(config):
    dl = Downloader()
    locs = dl.retrieve_localizations(config)

    return locs


def split_filter(predicate, arr):
    passing = []
    failing = []

    for item in arr:
        if predicate(item):
            passing += [item]
        else:
            failing += [item]

    return (passing, failing)


def make_localization_map(locs):
    localizations = {}
    for loc in locs:
        localizations[loc.key] = loc

    return localizations


def ensure_localization_uniqueness(locs):
    existing = set()
    duplicate = set()

    # if checking for duplicates, it's already in existing once
    allowed_duplicates = { 
        '..': 0 
    }

    print("Checking localization uniqueness")

    for loc in locs:
        if loc.key in existing:
            if loc.key in allowed_duplicates:
                allowed_duplicates[loc.key] += 1
            else:
                duplicate.add(loc.key)

        existing.add(loc.key)

    if len(duplicate) > 0:
        print("Found duplicate localizations:")
        for key in duplicate:
            print(" ", key)

        print()
        raise ValueError("Duplicate localizations found: {}".format(duplicate))

    for (key, repeats) in allowed_duplicates.items():
        if repeats > 1:
            print("  ? Note: key '{}' found {} times".format(key, repeats))

    print("Localizations verified.\n")



#===------------------------------------------------------------------------===#
# iOS

def get_ios_localizables(dir, config):
    localizables = []

    def is_localizable(filename):
        return filename.endswith('.strings')

    for root, directory, filenames in os.walk(dir):
        for filename in filenames:
            if is_localizable(filename) and not 'Base.lproj' in root:
                localizables += [iOSLocalizable(os.path.join(root, filename), config)]

    return localizables


def make_ios_localizations(base_localizations):
    return list(
        filter(lambda loc: loc.name is not None,
                map(lambda loc: iOSLocalization(loc), 
                    base_localizations)))


def main_ios(config, path):
    locs = make_ios_localizations(get_localizations(config))
    loc_map = make_localization_map(locs)
    ensure_localization_uniqueness(locs)
    localizer = iOSLocalizer(loc_map)
    
    localizables = get_ios_localizables(path, config)
    print("Localizing {} iOS files".format(len(localizables)))
    for localizable in localizables:
        localizer.localize(localizable)
    print("Done.")



#===------------------------------------------------------------------------===#
# Android

def get_android_localizables(dir, config):
    localizables = []

    def is_localizable(path_str):
        path = Path(path_str)
        return path.parent.stem.startswith('values') and \
            path.name.startswith('string') and \
            path.name.endswith('.xml')

    for root, directory, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if is_localizable(path):
                localizables += [AndroidLocalizable(path, config)]

    return localizables


def make_android_localizations(base_localizations):
    (item_locs, rest_locs) = \
        split_filter(lambda loc: loc.loc_type == 'item', base_localizations)

    localizations = \
        list(map(lambda loc: AndroidLocalization(loc), rest_locs))

    (android_specific_items, rest_items) = \
        split_filter(lambda loc: '-' not in loc.name, item_locs)

    def group_android_items(locs):
        groups = {}

        for loc in locs:
            groups[loc.name] = groups.get(loc.name, []) + [loc]

        return groups.values()

    localizations += \
        list(map(lambda locs: AndroidLocalization(locs), 
                group_android_items(android_specific_items)))

    def group_other_items(locs):
        groups = {}

        for loc in locs:
            loc_name = loc.name.split('-')[0]
            groups[loc_name] = groups.get(loc_name, []) + [loc]

        return groups.values()

    localizations += \
        list(map(lambda locs: AndroidLocalization(locs), 
                group_other_items(rest_items)))

    return localizations


def main_android(config, path):
    locs = make_android_localizations(get_localizations(config))
    loc_map = make_localization_map(locs)
    ensure_localization_uniqueness(locs)
    localizer = AndroidLocalizer(loc_map)
    
    localizables = get_android_localizables(path, config)
    print("Localizing {} Android files".format(len(localizables)))
    for localizable in localizables:
        localizer.localize(localizable)
    print("Done.")

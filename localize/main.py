#!/usr/bin/env python3
"""Localize

Localize an iOS or Android app's strings from a Sheetsu Google Sheet API.

Usage:
    localize (ios | android) [CONFIG]

Commands:
    ios         scan for and work with .strings files
    android     scan for and work with string*.xml files

Arguments:
    CONFIG      specify config file, [default: localize.yml]
"""

from docopt import docopt
from .config import Config
from .localize import main_ios, main_android
from os import getcwd



def main():
    args = docopt(__doc__)

    config_file = args['CONFIG'] or 'localize.yml'
    config = Config(config_file)

    if args['ios']:
        main_f = main_ios
    elif args['android']:
        main_f = main_android

    main_f(config, getcwd())


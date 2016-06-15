# Requirements

- ~> Python 3.5

# Installation

## Windows:

- In case fresh python install, add python to your `(Enviroment Settings).Path`
- Under localize root folder run `python setup.py install`
- Copy localize folder to `<python install dir>/lib/`
- Add `<python install dir>/Scripts` to your `(Enviroment Settings).Path`


## OS X

- Run `python3 setup.py install`
- No step 2


# Use

## Running

Navigate to an iOS or Android source directory which contains a `localize.yml` config file, and run:  

    localize <ios|android>

Alternatively, you can pass in another config file after the platform:  

    localize <ios|android> [CONFIG]


## Config

A [YAML][1] file that defines:

- supported languages
- default languages
- where to get localizations

### Example config from SMS Solutions

```YAML
languages:
    - English:  en
    - Dutch:    nl
    - French:   fr

default-language: en

sources:
    -   name: Common
        url: https://spreadsheets.google.com/feeds/list/1yQx7TLqeugzpY9JyjZw9mslBwJ6Pc8SDPdHBlMUlJ4w/2/public/values?alt=json
    -   name: Menu
        url: https://spreadsheets.google.com/feeds/list/1yQx7TLqeugzpY9JyjZw9mslBwJ6Pc8SDPdHBlMUlJ4w/3/public/values?alt=json
    -   name: Field User
        url: https://spreadsheets.google.com/feeds/list/1yQx7TLqeugzpY9JyjZw9mslBwJ6Pc8SDPdHBlMUlJ4w/4/public/values?alt=json
    -   name: Customer User
        url: https://spreadsheets.google.com/feeds/list/1yQx7TLqeugzpY9JyjZw9mslBwJ6Pc8SDPdHBlMUlJ4w/5/public/values?alt=json        
    -   name: Profile
        url: https://spreadsheets.google.com/feeds/list/1yQx7TLqeugzpY9JyjZw9mslBwJ6Pc8SDPdHBlMUlJ4w/6/public/values?alt=json
```

[1]: https://en.wikipedia.org/wiki/YAML
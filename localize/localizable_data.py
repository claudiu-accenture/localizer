#!/usr/bin/env python3



class LocalizableData:

    localization_key = None
    
    def __init__(self, localization_key):
        self.localization_key = localization_key



#===------------------------------------------------------------------------===#
# iOS

class iOSLocalizableData(LocalizableData):

    replacement_key = None

    def __init__(self, localization_key, replacement_key):
        super().__init__(localization_key)
        self.replacement_key = replacement_key

    def __repr__(self):
        return '{} = {}'.format(self.localization_key, self.replacement_key)




#===------------------------------------------------------------------------===#
# Android

class AndroidLocalizableData(LocalizableData):
    
    def __init__(self, localization_key, localizable_type=None):
        super().__init__(localization_key)
        self.localizable_type = localizable_type or 'string'

    def __repr__(self):
        localizable_type = self.localizable_type or 'string'
        return '{}: {}'.format(self.localization_key, localizable_type)

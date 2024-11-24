

class BaseValidator:
    def __init__(self, localization=None):
        self._localization = None
        self.set_localization(localization)

    def set_localization(self, localization):
        if localization:
            self._localization = localization
        else:
            from localizations.loc_RU import LocalizationConstants
            self._localization = LocalizationConstants



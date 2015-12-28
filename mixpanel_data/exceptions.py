class MixpanelError(Exception):
    pass


class MixpanelKeyInvalid(MixpanelError):
    pass


class MixpanelSecretInvalid(MixpanelError):
    pass


class MixpanelKeyMissing(MixpanelError):
    pass


class MixpanelSecretMissing(MixpanelError):
    pass


class MixpanelHTTPError(MixpanelError):
    pass


class MixpanelDataError(MixpanelError):
    pass

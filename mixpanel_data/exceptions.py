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
    def __init__(self, error):
        self.http_error_number = error.code
        self.response = error.fp.read()
        super(MixpanelHTTPError, self).__init__(str(error))


class MixpanelDataError(MixpanelError):
    pass

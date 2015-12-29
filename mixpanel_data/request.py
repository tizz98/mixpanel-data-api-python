import six
import json
import time
import hashlib
from six.moves import urllib

from . import exceptions


def set_key(key):
    if len(key) != 32:
        raise exceptions.MixpanelKeyInvalid(
            "API key must be 32 characters long.")
    Request._api_key = key


def set_secret(secret):
    if len(secret) != 32:
        raise exceptions.MixpanelSecretInvalid(
            "API secret must be 32 characters long.")
    Request._api_secret = secret


def set_key_and_secret(key, secret):
    set_key(key)
    set_secret(secret)


class Request(urllib.request.Request):
    _api_key = None
    _api_secret = None

    CURRENT_VERSION = '2.0'
    BASE_URL = 'mixpanel.com/api'
    RESPONSE_FORMAT = 'json'

    def __init__(self, endpoint, subdomain=None, version=None, secure=True,
                 json_decoder=None, lifetime_exp=3600, **params):
        self.endpoint = endpoint
        self.subdomain = subdomain

        if version is None:
            self.version = self.CURRENT_VERSION
        else:
            self.version = version

        self.secure = secure

        if json_decoder is None:
            self.json_decoder = json.loads
        else:
            self.json_decoder = json_decoder

        params['api_key'] = self.api_key
        params['expire'] = int(time.time()) + lifetime_exp
        params['format'] = self.RESPONSE_FORMAT

        if 'sig' in params:
            del params['sig']
        params['sig'] = self.hash_args(params)

        url = '{base_url}/{endpoint}/?{params}'.format(
            base_url=self.base_url,
            endpoint=self.endpoint,
            params=self.unicode_urlencode(params),
        )
        urllib.request.Request.__init__(self, url)
        print params
        print url

        self.lifetime = lifetime_exp

    @property
    def api_key(self):
        if self._api_key is None:
            raise exceptions.MixpanelKeyMissing(
                "API key must be specified before requests can be made.")
        return self._api_key

    @property
    def api_secret(self):
        if self._api_secret is None:
            raise exceptions.MixpanelSecretMissing(
                "API secret must be specified before requests can be made.")
        return self._api_secret

    @property
    def base_url(self):
        protocol = "https" if self.secure else "http"
        url = self.BASE_URL

        if self.subdomain is not None:
            url = "{sub}.{url}".format(sub=self.subdomain, url=url)

        return "{protocol}://{url}/{version}".format(
            protocol=protocol, url=url, version=self.version)

    def hash_args(self, args):
        """
            Hashes arguments by joining key=value pairs, appending a secret,
            and then taking the MD5 hex digest.
        """
        for arg in args:
            if isinstance(args[arg], list):
                args[arg] = json.dumps(args[arg])

        args_joined = ''

        for arg in sorted(args.keys()):
            if not isinstance(arg, six.text_type)\
               and isinstance(arg, six.string_types):
                args_joined += six.u(arg).encode("utf-8")
            else:
                args_joined += str(arg)

            args_joined += "="

            if not isinstance(args[arg], six.text_type)\
               and isinstance(args[arg], six.string_types):
                args_joined += six.u(args[arg]).encode("utf-8")
            else:
                args_joined += str(args[arg])

        print args_joined

        md5_hash = hashlib.md5(args_joined)
        md5_hash.update(self.api_secret)

        return md5_hash.hexdigest()

    @staticmethod
    def unicode_urlencode(params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()

        for idx, param in enumerate(params):
            if isinstance(param[1], list):
                params[idx] = (param[0], json.dumps(param[1]))

        data_to_encode = []

        for k, v in params:
            if not isinstance(v, six.text_type)\
               and isinstance(v, six.string_types):
                v = six.u(v).encode("utf-8")

            data_to_encode.append((k, v))

        return urllib.parse.urlencode(data_to_encode)

    def open(self):
        try:
            return urllib.request.urlopen(self)
        except urllib.error.HTTPError as e:
            raise exceptions.MixpanelHTTPError(e)

    def json(self):
        try:
            fp = self.open()
            data = self.json_decoder(fp.read().decode('utf-8'))
        except exceptions.MixpanelHTTPError as e:
            try:
                data = json.loads(e.response.decode('utf-8'))
            except Exception as e:
                raise exceptions.MixpanelError(e)

        return data

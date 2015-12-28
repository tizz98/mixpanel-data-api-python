import json
from datetime import datetime, date

import six

from . import exceptions
from .constants import PY_DATE_FORMAT, MP_DATE_FORMAT


def get_date_string(date_obj):
    if isinstance(date_obj, (datetime, date)):
            ret_obj = date_obj.strftime(PY_DATE_FORMAT)
    elif isinstance(date_obj, six.string_types):
        try:
            ret_obj = datetime.strptime(date_obj, PY_DATE_FORMAT)
        except ValueError:
            raise exceptions.MixpanelDataError(
                "from_date must be a datetime, date or string object"
                " formatted '%s'" % MP_DATE_FORMAT)
    else:
        raise exceptions.MixpanelDataError(
            "from_date must be a datetime, date or string object"
            " formatted '%s'" % MP_DATE_FORMAT)

    return ret_obj


def jsonl_decoder(s):
    data = []
    lines = s.split("\n")

    for line in lines:
        data.append(json.loads(line.rstrip('\r')))

    return data

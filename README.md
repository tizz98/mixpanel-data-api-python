# Mixpanel data
A simple python wrapper for the [Mixpanel data export api](https://mixpanel.com/docs/api-documentation/data-export-api).


## Installation
### From Source
- `git clone git@github.com:tizz98/mixpanel-data-api-python.git`
- `cd mixpanel-data-api-python`
- `python setup.py install` or `pip install .`

## Usage

#### Get Events in time frame
_from [mixpanel docs](https://mixpanel.com/docs/api-documentation/exporting-raw-data-you-inserted-into-mixpanel)_

```python
from datetime import date
import mixpanel_data

# Configure your api key and secret
mixpanel_data.set_key_and_secret(
    "API_KEY",
    "API_SECRET"
)

from_date = date(2015, 11, 1)
to_date = date(2015, 11, 2)

export = mixpanel_data.Export(from_date, to_date, 'Viewed report')
events = export.events

for event in events:
    print event.event  # Viewed report

    properties = event.properties

    print properties.distinct_id  # foo
    print properties.time  # 1329263748
```

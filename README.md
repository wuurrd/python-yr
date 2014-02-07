python-yr
=================
Library for the norwegian wheather service yr.no in python

### Usage
```python
from yr.libyr import Yr
import json

weather = Yr('Norge/Oslo/Oslo/Oslo', 'en')
temperature = weather.temperature()

print json.dumps(temperature, indent=4)
```
More example-usage can be found in the examples-folder :-)

### This returns
```json
{
    "credit": {
        "url": "http://www.yr.no/", 
        "text": "V\u00e6rvarsel fra yr.no, levert av NRK og Meteorologisk institutt"
    }, 
    "data": {
        "value": "14", 
        "unit": "celsius"
    }
}
```

More to come!

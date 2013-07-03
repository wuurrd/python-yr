python-yr
=================
Library for the norwegian wheather service yr.no in python

### Usage:
```python
from libyr import Yr
import json

weather = Yr('Oslo', 'en')
temperature = weather.temperature()

print json.dumps(temperature, indent=4)
```

More to come!

# fias

FIAS is supported by the following PMS systems from Oracle Hospitality: Oracle Hospitality Suite 8 (any version) &amp; Oracle Hospitality OPERA PMS (>= Ver. 4.x

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=atom-tr_fias-integration&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=atom-tr_fias-integration)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=atom-tr_fias-integration&metric=coverage)](https://sonarcloud.io/summary/new_code?id=atom-tr_fias-integration)

## Usage

```py
from fias.record import FIASRecord
# Extract data from FIAS broadcast message. Example
data = "GI|G#123|RN101|GNJohn Doe|DA241109|TI185700"

record = FIASRecord(data)
# check if record valid
try:
    record.is_valid(raise_exception=True)
except Exception as e:
    print(e)
else:
    # use record data
    print(record.GN)
```
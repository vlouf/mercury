# Mercury - A radiosounding data grabber

Mercury retrieves radiosounding data for a specified station at specified dates. For example:

```
from mercury import mercury

mercury(station_id='YPDN', bg_date='20140201', end_date='20140228')
```

It will download and save all radiosounding data for the Darwin (Australia) station between 1-Feb-2014 and 28-Feb-2014.

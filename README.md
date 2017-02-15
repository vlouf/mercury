# Mercury - A radiosounding data grabber

Mercury downloads radiosounding data for a specified station at specified dates from the University of Wyoming[1].

```
import mercury

mercury.mercury(station_id='YPDN', bg_date='20140201', end_date='20140228')
```

It will download and save all radiosounding data for the Darwin (Australia) station between 1-Feb-2014 and 28-Feb-2014.

If you want to know the list of available station and their id, just type:

```
mercury.station_list()
```

[1]: http://weather.uwyo.edu/upperair/sounding.html

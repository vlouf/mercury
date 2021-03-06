"""
.. module:: mercury
   :platform: Unix, Windows
   :synopsis: Retrieves radiosounding data for a specified station (e.g. YPDN
              for Darwin) at specified dates.

.. moduleauthor:: Valentin Louf <valentin.louf@bom.gov.au>


"""

import re
import os
import pickle
import string
import pandas
import datetime
import urllib.request

from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_sounding_data(kwargs):
    """
    Download radiosounding data from the University of Wyoming website.

    Parameters
    ----------
    the_date : datetime
        The date of the requested radiosoundings.
    the_hour : str
        The hour of radiosouding, either 00 or 12.
    station_id : str
        Radiosounding station ID (YPDN for Darwin)

    Returns
    -------
    data_dic : dict
        Dictionnary containing the data for the specified radiosouding and the
        filename associated.
    """

    the_date, the_hour, station_id = kwargs

    year= the_date.year
    month = the_date.month
    day = the_date.day

    if the_hour is not '00' and the_hour is not '12':
        print('Wrong time for radiosounding given, using "00" instead.')
        hour = '00'
    else:
        hour = the_hour  #either 12 or 00

    url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%' +\
          "3ALIST&YEAR=%i&MONTH=%02i&FROM=%02i%s&TO=%02i%s&STNM=%s" % \
          (year, month, day, hour, day, hour, station_id)

    with urllib.request.urlopen(url) as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    data_text = soup.get_text()
    splitted = data_text.split("\n",data_text.count("\n"))

    ascii_txt = "\n".join(splitted[4:])
    outfile = "%s_%i%02i%02i_%s.txt" % (station_id, year, month, day, hour)

    print("Sounding for " + station_id + " " + the_date.strftime("%d-%b-%Y") +
          " downloaded.")

    return {'filename':outfile, 'data':ascii_txt}


def mercury(station_id=None, bg_date=None, end_date=None, the_hour='00',
            outpath="soundings/", ncpu=1, save_ascii=False, save_pkl=True):
    """
    Retrieves radiosounding data.

    Parameters
    ----------
    station_id : str
        Radiosounding station ID (e.g. YPDN for Darwin)
    bg_date : str
        Begining date, format YYYYMMDD.
    end_date : str
        End date, format YYYYMMDD.
    the_hour : str
        The hour of radiosouding, either 00 or 12.
    outpath : str
        Output path to save data.
    ncpu : int
        Number of CPU on which the code will run.
    save_ascii : bool
        Save the results in separates ASCII text file.
    save_pkl : bool
        Save the results in a general pickle file.
    """

    if station_id is None:
        raise TypeError("Required argument station_id." +
                        "Call station_list() to get the list of station")

    if not os.path.exists(outpath):  # Check if output directory exists
        os.makedirs(outpath)

    the_daterange = pandas.date_range(bg_date, end_date)
    kwargs = [(dr, the_hour, station_id) for dr in the_daterange]

    with Pool(ncpu) as pool:
        rslt = pool.map(get_sounding_data, kwargs)

    if save_ascii:
        for rslt_slice in rslt:
            with open(outpath + rslt_slice['filename'], 'w+') as f:
                f.write(rslt_slice['data'])

    if save_pkl:
        with open(outpath + 'dwl_data.pkl', 'wb') as f:
            pickle.dump(rslt, f)

    return None


def station_list():
    """
    List all available stations and their id number.
    """

    maps = ['samer', 'europe', 'naconf', 'pac', 'nz', 'ant', 'np',
            'africa', 'seasia', 'mideast']

    desc = {'samer': 'South America',
            'europe': 'Europe',
            'naconf': 'North America',
            'pac': 'South Pacific',
            'nz': 'New Zealand',
            'ant': 'Antartica',
            'np': 'Artic',
            'africa': 'Africa',
            'seasia': 'South-East Asia',
            'mideast': 'Middle East'}

    for suffix in maps:
        url = "http://weather.uwyo.edu/upperair/%s.html" % (suffix)
        with urllib.request.urlopen(url) as f:
            content = f.read()
        soup = BeautifulSoup(content, "html.parser")

        st_id = []
        st_nm = []

        print(desc[suffix] + ":\n")
        print("\t\tStation id - Station name")

        for ar in soup.find_all('area'):
            st = ar.get('onmouseover')
            rgm = re.findall("[0-9]+", st)
            dgm = re.split("[0-9]+", st)
            try:
                st_nm.append(dgm[1][2:-2])
                st_id.append(rgm[0] )
                print("\t\t%s - %s" % (rgm[0], dgm[1][2:-2]))
            except IndexError:
                break

        print("\n")

    return None

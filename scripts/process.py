#!/usr/bin/python
import os
import csv
import urllib
import shutil
import logging
import re
import ssl
from functools import partial
import dataconverters

logger = logging.getLogger()

def setup():
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('archive'):
        os.makedirs('archive')

def find_links():
    '''Find all the download links in the page - they change every month'''
    url = 'http://eu.spindices.com/indices/real-estate/sp-case-shiller-us-national-home-price-index'
    content = urllib.urlopen(url).read()
    # download links are in dropdown from additional item page now
    # note in web browser they are "a" links but in curl etc they are <option>
    pattern = '<option [^>]+ value="([^"]*)">([^<]*)</option>'
    links = re.findall(pattern, content)
    # get both .xls links and .pdf links - we only want pdf
    links = [ l for l in links if '.xls' in l[0] ]
    return links

def retrieve():
    '''Retrieve the raw data to the local cache (archive directory)

    OK so we have to mess with ssl ... Why?

    So, let's walk through some steps

    1. We try to get a URL like
       http://www.spindices.com/documents/additionalinfo/20140826-107542/107542_cs-condoindices-0826.xls?force_download=true

    2. This redirects to an SSL URL
       (https://www.spice-indices.com/idpfiles/spice-assets/resources/public/documents/107542_cs-condoindices-0826.xls?force_download=true)

    3. If you try downloading this normally the code hangs (and times out)

    4. curl also hangs. With a bit of debugging you see it just hangs after
       reporting "SSLv3, TLS handshake, Client hello (1)"

    5. Fixed by adding -3 option to curl (forcing use of a specific ssl version
       AFAICT)
    
    6. A bit more use of interwebs suggests the hack below as a way to do this
       in python (and it works)
    '''
    # have monkey patch ssl - see notes in docstring
    # ssl.wrap_socket = partial(ssl.wrap_socket, ssl_version=ssl.PROTOCOL_SSLv3)

    for linkOffset, name in find_links():
        url = 'http://eu.spindices.com' + linkOffset
        fn = name.strip().lower().replace(' ', '-') + '.xls'
        dest = os.path.join('archive', fn)
        logger.info('Retrieving: %s' % url)
        urllib.urlretrieve(url, dest)
        logger.info('Saved to: %s' % dest)


def extract():
    '''Extract data from cached raw data files in archive and write to data/
    '''
    source = ['archive/home-price-index-levels.xls', 'archive/national-home-price-index-levels.xls']
    # all-month.csv might be more appropriate but we wanted to keep continuity
    # with cities-month.csv (before mid 2014 city data and national data were
    # provided separately but now there is just one file with everything) 
    out_path = ['data/cities-month.csv', 'data/national-month.csv']

    tmp_out = os.path.join('tmp', 'home-price-index-levels.csv'), os.path.join('tmp', 'national-home-price-index-levels.csv')
    for index in range(len(tmp_out)):
    	dataconverters.dataconvert(source[index], tmp_out[index], guess_types=False)
	
        indata = open(tmp_out[index]).read()
        # fix time in dataconvert which adds 00:00:00
        indata = indata.replace(' 00:00:00', '')
        indata = indata.replace('column_1', 'Date')
        indata = indata.split('\n')
        del indata[1]
        indata = '\n'.join(indata)
    	open(out_path[index], 'w').write(indata)

def process():
    setup()
    retrieve()
    extract()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    process()


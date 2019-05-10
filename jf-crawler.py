#!/usr/bin/env python
#from __future__ import unicode_literals
#from pattern.web import URL
import coloredlogs
coloredlogs.install()

import click
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

import logging
logger = logging.getLogger("main")

import random
from fake_useragent import UserAgent
import time

ran=False

import difflib
import math
import hashlib
import urllib2
import time
import os
import re
import os.path
import codecs
import io
import gzip
import unicodedata

from bs4 import BeautifulSoup

timeoutSec=30

def write_file_to_disk(raw_html_file):

    context=codecs.open('page.html','w',encoding='utf-8')
    context.write(raw_html_file)
    context.write('\n')
    context.close()

def write_result_to_disk(summary,output):

    context=codecs.open(output,'a',encoding='utf-8')
    context.write(summary)
    context.write('\n')
    context.close()

def remove_control_characters(s):
    return "".join(ch for ch in list(s) if unicodedata.category(ch)[0]!="C")


def decompress(bytes_seq):

    with open('page.gz', 'wb') as fil:
        fil.write(bytes_seq)
    #logger.info('page.gz is written.')

    with open('page.gz', 'rb') as fd:
        gzip_fd = gzip.GzipFile(fileobj=fd)
        raw_html_file=gzip_fd.read()
        write_file_to_disk(raw_html_file)

    return raw_html_file

def cleanup():
    if ran:
        os.remove('page.gz')
        os.remove('page.html')


def getRandomHeader():
    google_id = hashlib.md5(str(random.random())).hexdigest()[:16]
    ua = UserAgent()
    timestamp=int(time.time())

    randomHeader = { 'user-Agent': ua.random, 'cookie': 'GSP=LM=%d:S=%s' % (timestamp, google_id), 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.8', 'accept-encoding': 'gzip, deflate, sdch, br'}
    return randomHeader

def bs4_parsePage(gs_base_url):

    logger.info('url: %s',gs_base_url)

    request = urllib2.Request(gs_base_url, headers=getRandomHeader())
    response = urllib2.urlopen(request, timeout=timeoutSec)

    bytes_seq=response.read()

    rawfile=decompress(bytes_seq)

    gs_soup = BeautifulSoup(rawfile,"lxml")

    return gs_soup

@click.command()
@click.option('--city', '-c', type=click.Choice(['madrid', 'london', 'paris', 'amsterdam', 'berlin','barcelona']), default='madrid')
@click.option('--output', '-o', default='results',help='name of output file')
def run(city,output):

    logger.info('begin')

    counter=1

    baseurl='https://www.jobfluent.com'

    logger.info('city: %s',city)
    logger.info('output: %s',output)

    baseurl2=baseurl+'/jobs-'+city+'?page='

    #logger.info("baseurl: %s",baseurl)
    #logger.info("baseurl2: %s",baseurl2)
    ran=True

    for j in range(1, 11):

        pageurl=baseurl2+str(j)

        logger.warn('Page number: %d',j)

        soup=bs4_parsePage(pageurl)

        #logger.info("jf-file parsed.")


        data = soup.find_all("h3", {"class": "offer-title"})
        length = len(data)

        logger.info('I see %d offers on page %d.',length, j)


        for i in range(0, length):

            papersLeft=length-i
            logger.info("remaining offers:  %d",papersLeft)
            thisResult=""

            # get a element
            a_element=data[i].find("a",{"class":"text-no-decor"})

            # get job title
            title = ''.join(a_element.text).strip('\n').strip()
            logger.warn("Page number %d, Offer #%d",j,i)

            logger.info("Offer: %s",title)

            summary_url=baseurl+a_element.get('href')

            # open a job-description link
            jf_soup = bs4_parsePage(summary_url)

            # find job description element
            offer_element_list = jf_soup.find_all("div", {"itemprop": "description"})
            summary=''
            if len(offer_element_list) == 0:
                summary='missing-description'
                logger.error('I found no description for %s',title)
            else:
                offer_element = offer_element_list[0]
                p_elements=offer_element.find_all(text=True)
                for element in p_elements:
                    summary += ' ' + ''.join(element)

                summary=remove_control_characters(summary)
                summary=summary.replace('\n',' ').strip()

            write_result_to_disk(summary,output)

            logger.info('Summary length: %d',len(summary))

            time.sleep(1)

    logger.info('end.')

import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    run()

#!/usr/bin/env python3

import errno
import os
import re
from sys import argv
from time import sleep

import requests
from bs4 import BeautifulSoup


def get(url, referer=None):
    for i in range(1, 6):
        sleep(i / 2)
        headers = {}
        if referer:
            headers['Referer'] = referer
        resp = session.get(url, headers=headers)
        if resp.status_code == 200:
            return resp
        elif resp.status_code == 304:
            print('403')
        else:
            resp.raise_for_status()
    raise Exception('Repeated 403s while getting {}'.format(url))


image_page_regex = re.compile(r'http://([^.]*).deviantart.com/art/')
image_id_regex = re.compile(
    r'http://www.deviantart.com/download/([^/]*)/[^.]*\.([^?]*)')


if len(argv) == 1:
    raise Exception('You must pass a URL')

feed_url = argv[1]

created_dirs = set()

session = requests.Session()

while True:
    feed = BeautifulSoup(get(argv[1]).text, 'xml')

    for link in feed.find_all('link'):
        m = image_page_regex.match(link.text)
        if not m:
            continue
        deviant = m.group(1)
        if deviant not in created_dirs:
            try:
                os.mkdir(deviant)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            created_dirs.add(deviant)

        #print(link.text)
        #with open('page.html', 'wb') as f:
            #for chunk in get(link.text).iter_content(4000):
                #f.write(chunk)
        #exit(1)
        image_page = BeautifulSoup(get(link.text).text)
        for image_link in image_page.select('a.dev-page-download'):
            m = image_id_regex.match(image_link['href'])
            if not m:
                continue
            filename = deviant + '/' + m.group(1) + '.' + m.group(2)
            with open(filename, 'wb') as f:
                for chunk in get(image_link['href']).iter_content(4000):
                    f.write(chunk)
            print('{}: {}'.format(filename, image_link['href']))

    break

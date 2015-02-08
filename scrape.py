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
    r'http://www.deviantart.com/download/([^/]*)/([^.]*\.[^?]*)')


if len(argv) == 1:
    raise Exception('You must pass a URL')

feed_url = argv[1]

created_dirs = set()

session = requests.Session()

offset = 0

while True:
    print('offset = {}'.format(offset))
    feed = BeautifulSoup(
        get('{}&offset={}'.format(argv[1], offset)).text, 'xml')

    empty = True
    for link in feed.find_all('link'):
        m = image_page_regex.match(link.text)
        if not m:
            continue
        empty = False
        deviant = m.group(1)
        if deviant not in created_dirs:
            try:
                os.mkdir(deviant)
            except FileExistsError:
                pass
            created_dirs.add(deviant)

        image_page = BeautifulSoup(get(link.text).text)
        try:
            image_link = image_page.select('a.dev-page-download')[0]
        except IndexError:
            continue

        m = image_id_regex.match(image_link['href'])
        if not m:
            continue
        filename = deviant + '/' + m.group(1) + '_' + m.group(2)
        try:
            with open(filename, 'xb') as f:
                for chunk in get(image_link['href']).iter_content(4000):
                    f.write(chunk)
        except FileExistsError:
            print('already downloaded ' + filename)
            continue
        except:
            try:
                os.remove(filename)
            except:
                pass
            raise
        print(filename)
    if empty:
        print('Done')
        exit(0)

    offset += 60  # FIXME: Figure out how to detect this number.

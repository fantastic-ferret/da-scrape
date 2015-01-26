#!/usr/bin/env python3

import errno
import os
import re
import urllib.request
from sys import argv
from time import sleep

from bs4 import BeautifulSoup


def get(url):
    for i in range(1, 6):
        sleep(i / 2)
        try:
            return urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as e:
            if e.getcode() != 403:
                raise
            print('403')
    raise Exception('Repeated 403s while getting {}'.format(url))


def download(url, filename):
    for i in range(1, 6):
        sleep(i / 2)
        try:
            return urllib.request.urlretrieve(url, filename)
        except urllib.error.HTTPError as e:
            if e.getcode() != 403:
                raise
            print('403')
    raise Exception('Repeated 403s while getting {}'.format(url))


image_page_regex = re.compile(r'http://([^.]*).deviantart.com/art/')
image_id_regex = re.compile(
    r'http://www.deviantart.com/download/([^/]*)/[^.]*\.([^?]*)')


if len(argv) == 1:
    raise Exception('You must pass a URL')

feed_url = argv[1]

created_dirs = set()

while True:
    feed = BeautifulSoup(urllib.request.urlopen(argv[1]).read(), 'xml')

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

        image_page = BeautifulSoup(get(link.text))
        for image_link in image_page.select('a.dev-page-download'):
            m = image_id_regex.match(image_link['href'])
            if not m:
                continue
            filename = deviant + '/' + m.group(1) + '.' + m.group(2)
            print('{}: {}'.format(filename, image_link['href']))


    break

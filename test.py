#!/usr/bin/env python3

import urllib
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

if len(argv) == 1:
    raise Exception('You must pass a URL')

gallery_page_url = argv[1]
while True:
    gallery_page = BeautifulSoup(get(gallery_page_url))
    for image_page_link in gallery_page.select('a.thumb'):
        image_page = BeautifulSoup(get(image_page_link['href']))
        for image_link in image_page.select('a.dev-page-download'):
            print(image_link['href'])

    break

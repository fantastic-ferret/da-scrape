#!/usr/bin/env bash

set -o errexit

if ! [[ -d .env ]]; then
    virtualenv .env -p $(which python3)
fi

source .env/bin/activate


pip3 install beautifulsoup4==4.3.2 lxml==3.4.1 requests==2.5.1

#! /bin/sh
#
# runall.sh
# Copyright (C) 2016 michael_yin <michael_yin@mac.lan>
#
# Distributed under terms of the MIT license.
#

rm -rf ./release/*
scrapy list| xargs -n 1 scrapy crawl --loglevel=INFO -s FEED_URI='release/%(name)s.json'


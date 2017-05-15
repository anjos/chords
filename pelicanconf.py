#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'André Anjos'
SITENAME = 'Chords'
SITETITLE = 'Chords'
SITESUBTITLE = 'Songs & Collections'
SITEDESCRIPTION = 'Chordbook Website'
SITELOGO = '/images/profile_128.png'
FAVICON = '/images/favicon.ico'
SITEURL = 'http://chords.andreanjos.org'

# Theme setup
THEME = 'theme'
BROWSER_COLOR = '#333'

# Static directories
STATIC_PATHS = (
    'images',
    'pdfs',
    'css',
    )

# Extra CSS customization
EXTRA_PATH_METADATA = {
    'css/custom.css': {'path': 'css/custom.css'},
}
CUSTOM_CSS = 'css/custom.css'

ROBOTS = 'index, follow'

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
    }

PATH = 'content'
DELETE_OUTPUT_DIRECTORY = True

TIMEZONE = 'Europe/Zurich'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Links in the front page, aside from the static ``pages``
DIRECT_TEMPLATES = [
    'index',
    ]
LINKS = (
    ('Songs', '/songs/'),
    ('Artists', '/artists/'),
    ('Collections', '/collections/'),
    ('About', '/about/'),
    )

# Social widget
SOCIAL = (
    ('linkedin', 'https://www.linkedin.com/in/andreranjos/'),
    ('stack-overflow', 'https://stackoverflow.com/users/712525/andré-anjos'),
    ('github', 'https://github.com/anjos'),
    ('gitlab', 'https://gitlab.idiap.ch/bob'),
    ('skype', 'skype:andrezito?call'),
    )
GOOGLE_ANALYTICS = 'UA-37998740-1'

# Plugins
PLUGIN_PATHS = [
    'plugins',
    ]
PLUGINS = [
    'chords',
    ]

DEFAULT_PAGINATION = False
DISABLE_URL_HASH = True #don't put hashes by the end of urls
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
OUTPUT_RETENTION = [
    'CNAME',
    ]

# URL organization
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/.html'
PAGE_SAVE_AS = '{slug}/index.html'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

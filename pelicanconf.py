#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'André Anjos'
SITENAME = 'Cifras'
SITETITLE = 'Cifras'
SITESUBTITLE = 'Músicas & Coletâneas'
SITEDESCRIPTION = 'Website de Cifras'
SITELOGO = '/images/profile_128.png'
FAVICON = '/images/favicon.ico'
SITEURL = 'http://cifras.andreanjos.org'

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

DEFAULT_LANG = 'pt'
LOCALE = (
    'pt',
    )
DEFAULT_DATE_FORMAT = '%d/%m/%Y'
DATE_FORMATS = {
    'pt': '%d/%m/%Y',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Links in the front page, aside from the static ``pages``
DIRECT_TEMPLATES = [
    ]
LINKS = (
    ('Músicas', '/'),
    ('Artistas', '/artists/'),
    ('Coletâneas', '/collections/'),
    ('Download', '/cifras.pdf'),
    ('Sobre', '/sobre/'),
    )

# Social widget
SOCIAL = (
    ('linkedin', 'https://www.linkedin.com/in/andreranjos/'),
    ('stack-overflow', 'https://stackoverflow.com/users/712525/andré-anjos'),
    ('github', 'https://github.com/anjos'),
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

# URL organization for the chords plugin
ARTIST_LIST = 'artists/index.html'
ARTIST_URL = 'artists/{slug}/'
ARTIST_SAVE_AS = 'artists/{slug}/index.html'
SONG_LIST = 'index.html'
SONG_URL = 'songs/{slug}/'
SONG_SAVE_AS = 'songs/{slug}/index.html'
COLLECTION_LIST = 'collections/index.html'
COLLECTION_URL = 'collections/{slug}/'
COLLECTION_SAVE_AS = 'collections/{slug}/index.html'

# PDF organization
ARTIST_PDF_SAVE_AS = 'artist/{slug}/cifras.pdf'
SONG_PDF_SAVE_AS = 'songs/{slug}/cifra.pdf'
COLLECTION_PDF_SAVE_AS = 'collections/{slug}/cifras.pdf'
CHORDBOOK_PDF_SAVE_AS = 'cifras.pdf'

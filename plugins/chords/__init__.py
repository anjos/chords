#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Plugin initialization. See: http://docs.getpelican.com/en/stable/plugins.html#how-to-create-a-new-reader'''

from pelican import signals
from .generator import Generator

def _setup_generator(pelican_object):
  return Generator

def register():
  signals.get_generators.connect(_setup_generator)

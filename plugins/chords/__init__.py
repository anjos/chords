#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Plugin initialization. See: http://docs.getpelican.com/en/stable/plugins.html#how-to-create-a-new-reader'''

def register():
  from pelican import signals
  from .reader import ChordsReader as Reader
  def _setup(x):
    x.reader_classes['chords'] = Reader
  signals.readers_init.connect(_setup)

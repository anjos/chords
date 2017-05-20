#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Plugin initialization. See: http://docs.getpelican.com/en/stable/plugins.html#how-to-create-a-new-reader'''

import time
from pelican import signals
from .generator import Generator

def _setup_generator(pelican_object):
  return Generator

def _all_generators_finalized(generators):
  chords_gen = [k for k in generators if isinstance(k, Generator)][0]
  print('Done: Chords plug-in loaded information from {} artists, {} ' \
      'songs and {} collections in {:.2f} seconds.'.format(
        len(chords_gen.artists),
        len(chords_gen.songs),
        len(chords_gen.collections),
        time.time() - chords_gen.start,
        )
      )

def register():
  signals.get_generators.connect(_setup_generator)
  signals.all_generators_finalized.connect(_all_generators_finalized)

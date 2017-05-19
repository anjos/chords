#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Generator for artists, songs and collections

In Pelican, a generator controls the readout of files belonging to a particular
application. It may also accumulate them for later output generator.

'''

import os
import time
import datetime
import itertools
import yaml

import logging
logger = logging.getLogger(__name__)

import pelican.generators
import pelican.signals
import pelican.utils

from .contents import Artist, Song, Collection


_DEFAULT_SETTINGS = dict(
    CHORDS_ARTISTS_PATHS = [os.path.join('chords', 'artists')],
    CHORDS_ARTISTS_EXCLUDES = [],
    CHORDS_SONGS_PATHS = [os.path.join('chords', 'songs')],
    CHORDS_SONGS_EXCLUDES = [],
    CHORDS_COLLECTIONS_PATHS = [os.path.join('chords', 'collections')],
    CHORDS_COLLECTIONS_EXCLUDES = [],
    )


class Generator(pelican.generators.CachingGenerator):
  """Generate context for chords items (artists, songs and collections)"""

  def __init__(self, *args, **kwargs):
    self.artists = []
    self.songs = []
    self.collections = []
    self.start = time.time()
    super(Generator, self).__init__(*args, **kwargs)


  def generate_context(self):
    """Process all meaningful data for the chords application"""

    _artists = {}
    _songs = {}
    _collections = {}

    for klass, _dict in ((Artist, _artists), (Song, _songs), (Collection,
      _collections)):

      paths = 'CHORDS_%sS_PATHS' % klass.__name__.upper()
      paths = self.settings.get(paths, _DEFAULT_SETTINGS[paths])
      excludes = 'CHORDS_%sS_EXCLUDES' % klass.__name__.upper()
      excludes = self.settings.get(excludes, _DEFAULT_SETTINGS[excludes])
      container = getattr(self, '%ss' % klass.__name__.lower())

      for f in self.get_files(paths, excludes, extensions=['yml', 'yaml']):

        obj = self.get_cached_data(f, None)

        if obj is None: # try to load it from disk

          try:

            path = os.path.join(self.path, f)
            with pelican.utils.pelican_open(path) as _file:
              data = yaml.load(_file)
              # transform date objects in datetime to improve pelican compat.
              for key, value in data.items():
                if isinstance(value, datetime.date):
                  data[key] = datetime.datetime.combine(value,
                      datetime.time(0,0))
              obj = klass('', data, self.settings, f, self.context)

          except Exception as e:
              logger.error(
                  'Could not process %s\n%s', f, e,
                  exc_info=self.settings.get('DEBUG', False))
              self._add_failed_source_path(f)
              continue

          # setup slug for chord objects
          setattr(obj, 'slug', getattr(obj, 'slug',
            os.path.basename(os.path.splitext(obj.source_path)[0])))

          if klass == Artist:
            setattr(obj, 'songs', [])

          if klass == Song:
            for artist in ('performer', 'composer'):
              slug = data.get('%s-slug' % artist)
              if slug is not None:
                if slug in _artists:
                  setattr(obj, artist, _artists[slug])
                  if obj not in _artists[slug].songs:
                    _artists[slug].songs.append(obj)
                else:
                  logger.error('Could not process %s\nCannot link %s', f,
                      artist)
                  self._add_failed_source_path(f)
                  continue

          if klass == Collection:
            setattr(obj, 'songs', [])
            for slug in obj.metadata['song-slugs']:
              if slug in _songs:
                obj.songs.append(_songs[slug])
              else:
                logger.error('Could not process %s\nCannot link %s', f, slug)
                self._add_failed_source_path(f)
                continue

          self.cache_data(f, obj)

        container.append(obj)
        self.add_source_path(obj)
        _dict[obj.slug] = obj

    self._update_context(('artists', 'songs', 'collections'))
    self.save_cache()
    self.readers.save_cache()
    pelican.signals.page_generator_finalized.send(self)


  def _generate_indexes(self, writer):
    """Generate pages allowing the user to nagivate from object to object"""

    for model, objects in ((Artist, self.artists), (Song, self.songs),
        (Collection, self.collections)):
      name = model.__name__.lower()
      save_as = self.settings.get("%s_LIST" % name.upper(),
          "%ss/index.html" % name)
      writer.write_file(
          save_as,
          self.get_template(model.list_template),
          self.context,
          objects=objects,
          relative_urls=self.settings['RELATIVE_URLS'],
          )


  def _generate_objects(self, writer):
    """Generate pages related to each indivual modelled object

    This method will respect user settings for the location of pages. The name
    of templates is taken from the corresponding class static variables.
    """

    # writes specific
    for obj in itertools.chain(self.artists, self.songs, self.collections):
      writer.write_file(
          obj.save_as,
          self.get_template(obj.template),
          self.context,
          object=obj,
          relative_urls=self.settings['RELATIVE_URLS'],
          override_output=hasattr(obj, 'override_save_as'),
          )
      pelican.signals.page_writer_finalized.send(self, writer=writer)


  def generate_output(self, writer):
    """Called by pelican as part of the generator interface

    Should trigger the generation of all required documents.
    """

    self._generate_objects(writer)
    self._generate_indexes(writer)

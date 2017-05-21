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
import pkg_resources

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

_UNKNOWN_IMAGE_PATH = pkg_resources.resource_filename(__name__,
    os.path.join('img', 'unknown.jpg'))

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
            # use this image for the artist
            img = os.path.splitext(path)[0] + '.jpg'
            if not os.path.exists(img): img = _UNKNOWN_IMAGE_PATH
            setattr(obj, 'image_path', img)

            # initializes song list
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

    # re-organize artists and collections - by slug
    self.songs.sort(key=lambda x: x.slug)
    for k in self.artists: k.songs.sort(key=lambda x: x.slug)
    for k in self.collections: k.songs.sort(key=lambda x: x.slug)

    self._update_context(('artists', 'songs', 'collections'))
    self.save_cache()
    self.readers.save_cache()
    pelican.signals.page_generator_finalized.send(self)


  def _generate_pdf(self):
    """Generate pdf pages for specific entries"""

    import time

    from .pdf import chordbook, song

    baseurl = self.settings.get('SITEURL', '/')
    output = self.settings.get('OUTPUT_PATH', 'output')
    author = self.settings.get('AUTHOR', 'Unknown Editor')

    # all chords
    start = time.time()
    basename = self.settings.get('CHORDBOOK_PDF_SAVE_AS', 'pdfs/chordbook.pdf')
    filename = os.path.join(output, basename)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname): os.makedirs(dirname)

    doc = chordbook(filename, self.songs, 'Cifras por', author,
        '/'.join((baseurl, basename)), self.settings)
    print('Done: Chords plug-in processed site-wide PDF in {:.2f} ' \
        'seconds'.format(time.time()-start))

    # per artist
    start = time.time()
    for k in self.artists:
      if len(k.songs) == 0:
        print('Skip: Chords plug-in skipped artist %s - no songs' % k.slug)
        continue
      basename = self.settings.get('ARTIST_PDF_SAVE_AS',
          'pdfs/artists/{slug}.pdf')
      basename = basename.format(slug=k.slug)
      filename = os.path.join(output, basename)
      dirname = os.path.dirname(filename)
      if not os.path.exists(dirname): os.makedirs(dirname)
      doc = chordbook(filename, k.songs, 'Cifras de %s' % k.name,
          'por %s' % author, '/'.join((baseurl, basename)), self.settings)
      setattr(k, 'pdf_url', basename)
    print('Done: Chords plug-in processed {} artist PDFs in {:.2f} ' \
        'seconds'.format(len(self.artists), time.time()-start))

    # per song
    start = time.time()
    for k in self.songs:
      basename = self.settings.get('SONG_PDF_SAVE_AS', 'pdfs/songs/{slug}.pdf')
      basename = basename.format(slug=k.slug)
      filename = os.path.join(output, basename)
      dirname = os.path.dirname(filename)
      if not os.path.exists(dirname): os.makedirs(dirname)
      doc = song(filename, k, self.settings)
      setattr(k, 'pdf_url', basename)
    print('Done: Chords plug-in processed {} song PDFs in {:.2f} ' \
        'seconds'.format(len(self.songs), time.time()-start))

    # per collection
    start = time.time()
    for k in self.collections:
      if len(k.songs) == 0:
        print('Skip: Chords plug-in skipped collection %s - no songs' % k.slug)
        continue
      basename = self.settings.get('COLLECTION_PDF_SAVE_AS',
          'pdfs/collections/{slug}.pdf')
      basename = basename.format(slug=k.slug)
      filename = os.path.join(output, basename)
      dirname = os.path.dirname(filename)
      if not os.path.exists(dirname): os.makedirs(dirname)
      doc = chordbook(filename, k.songs, 'Cifras da Coletânea %s' % k.title,
          'por %s' % author, '/'.join((baseurl, basename)), self.settings)
      setattr(k, 'pdf_url', basename)
    print('Done: Chords plug-in processed {} collection PDFs in {:.2f} ' \
        'seconds'.format(len(self.collections), time.time()-start))


  def _generate_indexes(self, writer):
    """Generate pages allowing the user to nagivate from object to object"""

    for model, objects in ((Artist, self.artists), (Song, self.songs),
        (Collection, self.collections)):
      objects = objects if model == Song else [k for k in objects if k.songs]
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
      if isinstance(obj, (Artist, Collection)) and not obj.songs:
        print('Skip: Chords plug-in skipped %s %s - no songs' % \
            (obj.__class__.__name__.lower(), obj.slug))
        continue
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

    self._generate_pdf() #this has to come first so pdf_urls are set
    self._generate_objects(writer)
    self._generate_indexes(writer)

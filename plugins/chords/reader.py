#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Definition of the Chords base reader class for Pelican'''


from pelican.readers import BaseReader
from .models import Artist, Song, Collection


class ChordsReader(BaseReader):

  enabled = True
  file_extensions = ['yml', 'yaml']


  def read(self, filename):
    '''Loads file contents returns summary and parsed info on node

    This method will use our classes to load information from yaml files. It
    will return parsed information from the author, song or collection being
    loaded.

    Parameters:

      filename (str): Full path to the file to load


    Returns:

      str: The content of the loaded article (this should be in HTML, without
      special markup added so it can be customized by the user)

      dict: A dictionary containing the parsed metadata for the file. Should
      contain, at least a ``title``, ``category`` and ``date``.

    '''

    if 'artists' in filename: cls = Artist
    elif 'songs' in filename: cls = Song
    elif 'collections' in filename: cls = Collection
    else:
      raise RuntimeError('can only read articles in a category folder named' \
          ' either "artists", "songs" or "collections" -- %s is not valid' \
          % filename)

    obj = cls(filename)

    # normalize to make pelican happy
    parsed = obj.as_dict()
    for key, value in obj.as_dict().items():
      parsed[key] = self.process_metadata(key, value)

    return obj.content, parsed

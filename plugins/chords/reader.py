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

      str: A summary of what was loaded
      dict: A dictionary containing the parsed metadata for the file. Should
      contain, at least a ``title``, ``category`` and ``date``.
    '''

    import ipdb; ipdb.set_trace()

    metadata = {
        'title': 'Oh yeah',
        'category': 'Foo',
        'date': '2012-12-01',
        }

    parsed = {}
    for key, value in metadata.items():
      parsed[key] = self.process_metadata(key, value)

    return "Some content", parsed

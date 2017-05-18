#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Base classes defining the component model for this plugin'''


import pelican.contents

from . import parser


class Artist(pelican.contents.Content):
  '''An artist is a group or individual that can perform or compose a song
  '''

  mandatory_properties = ('name',)
  default_template = 'artist'
  list_template = 'artists'


class Song(pelican.contents.Content):
  '''A Song corresponds to the title, lyrics and chords of a music
  '''

  mandatory_properties = ('title', 'tone', 'song')
  default_template = 'song'
  list_template = 'songs'


  @property
  def two_columns(self):

    return self.metadata.get('two-columns', False)


  def items(self):
    '''Parses and returns the lines of the song as specialized items'''

    return parser.syntax_analysis(parser.parse(self.song))


  def items_by_column(self):
    '''The same as ``items()``, but with 2 columns'''

    i = self.items()
    if len(i) <= 1: return i
    #else, we can split it better
    cut = int(round(len(i)/2))
    if len(i)%2 == 1:
      #if the number of elements is odd, put more on the first column
      cut += 1
    return (i[:cut], i[cut:])



class Collection(pelican.contents.Content):
  '''A collection corresponds to a list of songs with a name
  '''

  mandatory_properties = ('title', 'song-slugs')
  default_template = 'collection'
  list_template = 'collections'

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Base classes defining the component model for this plugin'''


import pelican.contents


class Artist(pelican.contents.Content):
  '''An artist is a group or individual that can perform or compose a song
  '''

  mandatory_properties = ('name',)
  default_template = 'artist'


class Song(pelican.contents.Content):
  '''A Song corresponds to the title, lyrics and chords of a music
  '''

  mandatory_properties = ('title', 'tone', 'song')
  default_template = 'song'


class Collection(pelican.contents.Content):
  '''A collection corresponds to a list of songs with a name
  '''

  mandatory_properties = ('title', 'song-slugs')
  default_template = 'collection'

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

'''Base classes defining the component model for this plugin'''


import os
import yaml
import datetime


def _basename(filename):
  '''Returns the basename w/o the extension for a given filename'''
  return os.path.splitext(os.path.basename(filename))[0]


class Artist(object):
  '''An artist is a group or individual that can perform or compose a song


  Parameters:

     filename (str): Full path to the file to load

  '''


  def __init__(self, filename):
    with open(filename) as f:
      data = yaml.load(f)

      # name is obligatory
      assert 'name' in data, 'name attribute not found at %s' % (filename,)
      self.name = data['name']

      # these are optional
      self.color = data.get('color', 0x000000)
      self.slug = data.get('slug', _basename(filename))
      self.category = 'artists'


  def __str__(self):
    return self.name


  def as_dict(self):
    return dict(
        title = self.name, #to make pelican happy
        date = datetime.date.today().strftime('%Y-%m-%d'),
        name = self.name,
        color = self.color,
        slug = self.slug,
        category = self.category,
        )


class Song(object):
  '''A Song corresponds to the title, lyrics and chords of a music


  Parameters:

     filename (str): Full path to the file to load

  '''


  def __init__(self, filename):

    with open(filename) as f:
      data = yaml.load(f)

      assert 'title' in data, 'title attribute not found in %s' % (filename,)
      assert 'tone' in data, 'tone attribute not found in %s' % (filename,)
      assert 'song' in data, 'song attribute not found in %s' % (filename,)

      # if the minimal validates, load the song
      self.title = data['title']
      self.tone = data['tone']
      self.song = data['song']

      self.date = data.get('date')
      self.modified = data.get('modified')
      self.year = data.get('year') #year the song was composed in
      self.performer_slug = data.get('performer-slug')
      self.composer_slug = data.get('composer-slug')
      self.two_columns = data.get('two-columns') #should be drawn in 2-columns
      self.slug = data.get('slug', _basename(filename))
      self.category = 'songs'

      # transform into datetime as pelican requires it
      if self.date: self.date = self.date.strftime('%Y-%m-%d')
      if self.modified: self.modified = self.modified.strftime('%Y-%m-%d')


  def __str__(self):
    return '%s (in %s)' % (self.title, self.tone)

  def as_dict(self):
    return dict(
        title = self.title,
        tone = self.tone,
        song = self.song,
        date = self.date,
        modified = self.modified,
        year = self.year,
        performer_slug = self.performer_slug,
        composer_slug = self.composer_slug,
        two_columns = self.two_columns,
        slug = self.slug,
        category = self.category,
        )


class Collection(object):
  '''A collection corresponds to a list of songs with a name


  Parameters:

     filename (str): Full path to the file to load

  '''


  def __init__(self, filename):
    with open(filename) as f:
      data = yaml.load(f)

      assert 'title' in data, 'title attribute not found at %s' % (filename,)
      assert 'date' in data, 'date attribute not found at %s' % (filename,)
      assert 'modified' in data, 'modified attribute not found at %s' % \
          (filename,)
      assert 'song-slugs' in data, \
          'song-slugs attribute not found at %s' % (filename,)

      self.title = data['title']
      self.date = data.get('date')
      self.modified = data.get('modified')
      self.song_slugs = data['song-slugs']
      self.category = 'collections'
      self.slug = data.get('slug', _basename(filename))

      # transform into datetime as pelican requires it
      if self.date: self.date = self.date.strftime('%Y-%m-%d')
      if self.modified: self.modified = self.modified.strftime('%Y-%m-%d')


  def __str__(self):
    return '%s (%d songs)' % (self.title, len(self.song_slugs))


  def as_dict(self):
    return dict(
        title = self.title,
        date = self.date,
        modified = self.modified,
        song_slugs = self.song_slugs,
        slug = self.slug,
        category = self.category,
        )

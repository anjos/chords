.. image:: https://travis-ci.org/anjos/chords.svg?branch=master
   :target: https://travis-ci.org/anjos/chords

----------------
 Chords Website
----------------

Generator code using Pelican_, for my private web site for song chords. The
website is re-built at every commit and re-deployed as Github Pages via
Travis_.


Local Testing
-------------

It is possible to locally test the web site before commit/pushing it back to
GitHub (which will case the site to be re-compiled and re-deployed). I advise
you to install a Conda_-based environment for deployment with this command
line::

  $ conda env create -f env.yml
  $ source activate site


To compile a new version of the website, do::

  $ pelican

To test the website, do::

  $ ./develop_server.sh start 8000

Use the application ``develop_server.sh`` to restart the server or stop it if
necessary.

.. note::

   The application ``develop_server.sh`` is provided by ``pelican-quickstart``.
   You should regenerate it in case of problems.


Deployment
----------

Deployment is automatic, once you push a tag to github. Deployment instructions
are stored in ``.travis.yml``.


Plugin Development
------------------

Chords is a Pelican plugin that allows you to create and manage lyrics and
chords as in an electronic chordbook.

* Defines the concept of a song and a structured way to express chords on it
* Can be organized by Artist or Collections.
* Can export PDFs using Reportlab
* Some level of customization for the artist appearance


Chordpro Format
===============

Pelican-chords stores songs in the chordpro format, a simple format for
notation of lyrics together with chords. Use your popular Internet search
engine to find huge collections of songs in chordpro format in the Word Wide
Web.

In the chordpro format chords are denoted in square brackets [] in the text,
e.g.::

  [Em]Alas, my [G]love, you [D]do me [Bm]wrong,

Should be rendered as something like this::

  Em       G         D     Bm
  Alas, my love, you do me wrong,

Jumping one or more lines, defines a verse.

In addition to the chords in square brackets, the chordpro format defines
several control sequences in curly brackets (``{}``). Pelican-chords
understands the following control statements:

* ``{comment: ...}`` or ``{c: ...}`` - **Comment**, e.g. Repeat 2x or Chorus.
  Comments are rendered inverse.
* ``{soc}``, ``{start_of_chorus}`` and ``{eoc}``, ``{end_of_chorus}``- **Start
  and end of chorus**. The chorus is indicated by a black line to the left.
* ``{sot}``, ``{start_of_tab}`` and ``{eot}``, ``{end_of_tab}`` Start and end
  of tab. A tab (tablature) section is rendered in a fixed width font.
* Lines starting with a hash-mark (``#``) are comment lines and are ignored in
  the song view.

Note the control sequences cannot be combined on the same line with the lyrics.

The following statements are ignored by Pelican-chords as we have special
database fields for those.

* ``{define ...}`` Used to define a special chord for this song. The chord
  format is ``<chord name> <base fret> <string 6> ...<string 1>``, e.g. ``G 1 3
  2 0 0 0 3``
* ``{title: ...}`` or ``{t: ...}`` - **Song title**. This is displayed in the
  song list screen and in the title bar.
* ``{subtitle: ...}`` or ``{st: ...}`` Song subtitle, typically the interpret
  or composer. This is displayed in the song list screen and in the title bar.


.. Place your references after this line
.. _conda: http://conda.pydata.org/miniconda.html
.. _pelican: http://getpelican.com
.. _travis: https://docs.travis-ci.com

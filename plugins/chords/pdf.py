#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""PDF generation for chords.
"""

import os
import datetime
import PIL
import contextlib

# the pdf generation stuff
from reportlab.platypus import Paragraph, XPreformatted, Spacer, CondPageBreak
from reportlab.platypus.flowables import NullDraw
from reportlab.platypus import NextPageTemplate
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

style = {}

fontsize = 10 #points

# This is an estimation of the number of characters that fits in a
# single-column document with a fontsize as indicated above. We have no
# heuristic to calculate how many there should be so, we have to create a
# document and count.
colwidth = {'single': 85, 'double': 41}

style['normal'] = ParagraphStyle(name='normal',
                                 fontName='Times-Roman',
                                 fontSize=fontsize,
                                 leading=int(1.3 * fontsize),
                                 leftIndent=0,
                                 allowWidows=0,
                                 allowOrphans=0)

style['cover-title'] = ParagraphStyle(name='cover-title',
                                parent=style['normal'],
                                fontSize=3 * fontsize,
                                alignment=TA_CENTER,
                                leading=int(3.6 * fontsize))

style['cover-subtitle'] = ParagraphStyle(name='cover-subtitle',
                                         parent=style['normal'],
                                         fontSize=1.8 * fontsize,
                                         textColor = Color(0.3, 0.3, 0.3, 1),
                                         alignment=TA_CENTER,
                                         leading=int(3.6 * fontsize))

style['toc-entry'] = ParagraphStyle(name='toc-entry',
                                    parent=style['normal'],
                                    fontSize=1.5 * fontsize,
                                    textColor = Color(0.3, 0.3, 0.3, 1),
                                    leading=int(1.8 * fontsize))

style['song-title'] = ParagraphStyle(name='song-title',
                                parent=style['normal'],
                                fontSize=2 * fontsize,
                                leading=int(2.6 * fontsize))

style['tone'] = ParagraphStyle(name='tone',
                               parent=style['normal'],
                               fontName='Times-Italic',
                               font = int(1.5 * fontsize),
                               leading = int(1.7 * fontsize))

style['verse'] = ParagraphStyle(name='verse',
                                 parent=style['normal'],
                                 fontName='Courier')

style['tablature'] = ParagraphStyle(name='tablature',
                                    parent=style['verse'],
                                    textColor = Color(0, 0.67, 0, 1),
                                    fontName='Courier-Bold',
                                    spaceBefore = fontsize,
                                    spaceAfter = fontsize)

style['chorus'] = ParagraphStyle(name='chorus',
                                 parent=style['verse'],
                                 textColor = Color(0.67, 0, 0, 1),
                                 fontName = 'Courier-Bold',
                                 spaceBefore = fontsize,
                                 spaceAfter = fontsize)

style['comment'] = ParagraphStyle(name='comment',
                                  parent=style['verse'],
                                  textColor = Color(0.67, 0.67, 0.67, 1),
                                  fontName = 'Courier-Oblique')


def tide(story, doc):
  """This method will pre-calculate the size of the following flowable and
  force a page break on the story if the space available is not enough to
  contain the flowable. This avoids the break-up verses, choruses and
  tablatures."""

  retval = []
  frame_width = doc.width - doc.leftMargin - doc.rightMargin
  frame_height = doc.height - doc.topMargin - doc.bottomMargin
  for k in story:
    if not retval:
      retval.append(k)
      continue

    width, height = k.wrap(frame_width, frame_height)
    retval.append(CondPageBreak(height))
    retval.append(k)

  return retval


def page_circle_center(x, y, fontsize, value):
  """Calculates the approximate circle center given the page positioning,
  fontsize and its current value."""
  length = len(str(value)) #the field length

  if length == 1: #only one digit in the page
    return x+0.25*fontsize, y+0.35*fontsize
  elif length == 2: #two digits in the page
    return x+0.5*fontsize, y+0.35*fontsize
  elif length == 3: #three digits
    return x+0.75*fontsize, y+0.35*fontsize
  elif length == 4: #four digits
    return x+fontsize, y+0.35*fontsize
  #how many songs do you intend to have??
  return x+2*fontsize, y+0.35*fontsize


def _cover_page(canvas, doc):
  """Defines the cover page layout."""

  from reportlab.lib.units import cm

  canvas.saveState()

  # draws the rectangle with the site name in vertical form
  # remember: coordinates (0,0) start at bottom left and go up and to the
  # right!
  canvas.setFillGray(0)
  page_height = doc.bottomMargin + doc.height + doc.topMargin
  page_width = doc.leftMargin + doc.width + doc.rightMargin
  x = page_width - doc.leftMargin
  rect_width = page_width - x
  canvas.rect(x, 0, rect_width, page_height, fill=True, stroke=False)

  canvas.rotate(90)
  t = canvas.beginText()
  font_size = 20
  t.setTextOrigin(doc.bottomMargin, -x-font_size-2)
  t.setFont('Times-Bold', font_size)
  t.setFillGray(0.75)
  t.textLine(u"http://cifras.andreanjos.org")
  canvas.drawText(t)

  canvas.restoreState()


def toc_page(canvas, doc):
  from reportlab.lib.colors import Color
  from reportlab.lib.units import cm

  canvas.saveState()

  # draws the rectangle saying "Table of Contents", in black
  # remember: coordinates (0,0) start at bottom left and go up and to the
  # right!
  canvas.setFillGray(0.0)
  page_height = doc.bottomMargin + doc.height + doc.topMargin
  page_width = doc.leftMargin + doc.width + doc.rightMargin
  y = page_height - doc.topMargin + 0.2*cm # a bit above the top margin
  rect_height = page_height - y
  canvas.rect(0, y, page_width, rect_height, fill=True, stroke=False)

  name = canvas.beginText()
  name.setTextOrigin(doc.leftMargin, y+0.4*cm)
  name.setFont('Helvetica-Bold', 20)
  name.setFillGray(1)
  name.textLine('Conteúdo')
  canvas.drawText(name)


  def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """
    if not isinstance(input, type(1)):
      raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
      raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
      count = int(input / ints[i])
      result.append(nums[i] * count)
      input -= ints[i] * count
    return ''.join(result)


  def page_circle_center(x, y, fontsize, value):
    """Calculates the approximate circle center given the page positioning,
    fontsize and its current value."""
    length = len(str(value)) #the field length

    if length == 1: #only one digit in the page
      return x+0.15*fontsize, y+0.35*fontsize
    elif length == 2: #two digits in the page
      return x+0.30*fontsize, y+0.35*fontsize
    return x+0.45*fontsize, y+0.35*fontsize

  # Draws song name and page number
  page_x = doc.width+doc.rightMargin+0.2*cm
  page_y = doc.bottomMargin-(0.1*cm)
  page_fontsize = 11
  page = canvas.beginText()
  page.setTextOrigin(page_x, page_y)
  page.setFont('Helvetica-Bold', page_fontsize)
  page.setFillGray(1)
  page_number = int_to_roman(doc.page).lower()
  page.textLine(page_number)

  #circle around number
  canvas.setFillGray(0.0)
  circle_x, circle_y = page_circle_center(page_x, page_y,
      page_fontsize, page_number)
  canvas.circle(circle_x, circle_y, 1.5*page_fontsize, fill=True,
      stroke=False)

  canvas.drawText(page)

  canvas.restoreState()


def set_basic_templates(doc):
  from reportlab.platypus.frames import Frame
  from reportlab.platypus.doctemplate import PageTemplate
  from reportlab.lib.units import cm

  doc._calc() #taken from reportlab source code (magic)

  templates = []

  #the front page framing
  cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
      leftPadding=0, rightPadding=10, topPadding=3*cm, bottomPadding=5*cm)
  templates.append(PageTemplate(id='Cover', frames=cover_frame,
    onPage=_cover_page, pagesize=doc.pagesize))

  #normal frame, for the TOC
  frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
      id='normal', rightPadding=0, leftPadding=0)
  templates.append(PageTemplate(id='TOC', frames=frame, onPage=toc_page,
    pagesize=doc.pagesize))

  doc.addPageTemplates(templates)


class SongTemplate(BaseDocTemplate):

  def __init__(self, *args, **kwargs):
    from reportlab.lib.units import cm

    kwargs.setdefault('leftMargin', 1.5 * cm)
    kwargs.setdefault('rightMargin', 1.5 * cm)
    kwargs.setdefault('bottomMargin', 1.5 * cm)

    BaseDocTemplate.__init__(self, *args, **kwargs)


class SongBookTemplate(BaseDocTemplate):


  def __init__(self, *args, **kwargs):
    from reportlab.lib.units import cm

    kwargs.setdefault('leftMargin', 1.5 * cm)
    kwargs.setdefault('rightMargin', 1.5 * cm)
    kwargs.setdefault('bottomMargin', 1.5 * cm)

    BaseDocTemplate.__init__(self, *args, **kwargs)
    set_basic_templates(self)


  def afterFlowable(self, flowable):
    """Registers TOC entries in our Doc Templates."""

    if flowable.__class__.__name__ == 'Paragraph' and \
        flowable.style.name == 'song-title':
      key = 'song-title-%s' % self.seq.nextf('song-title')
      self.canv.bookmarkPage(key)
      self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, key))


def cover_page(title, subtitle, url, siteurl, dateformat):
  """Bootstraps our PDF sequence of flowables."""

  from reportlab.platypus import Paragraph, Spacer, PageBreak
  from reportlab.lib.units import cm

  story = []
  story.append(Paragraph('<i>%s</i><br/><b>%s</b>' % (title, subtitle),
      style['cover-title']))
  story.append(Spacer(1, 3*cm))

  story.append(Paragraph('Compilado <b>%s</b><br/>%s' % \
      (datetime.date.today().strftime(dateformat), url),
      style['cover-subtitle']))
  return story


class PdfSong(object):
  """A container for a song object that can interact with ReportLab to
  genererate PDFs


  Parameters:

    song (Song): a song object

    dateformat (str): The format of the date to use for PDF generation

  """


  def __init__(self, song, dateformat):
    self.song = song
    self.dateformat = dateformat


  def basic_page(self, canvas, doc):
    """Sets elements that are common to all song PDF pages in django-chords."""

    from reportlab.lib.colors import Color
    from reportlab.lib.units import cm
    import pkg_resources

    # draws the rectangle with the performer name and picture
    # remember: coordinates (0,0) start at bottom left and go up and to the
    # right!
    canvas.setFillColor(self.performer_color())
    page_height = doc.bottomMargin + doc.height + doc.topMargin
    page_width = doc.leftMargin + doc.width + doc.rightMargin
    y = page_height - doc.topMargin + 0.2*cm # a bit above the top margin
    rect_height = page_height - y
    canvas.rect(0, y, page_width, rect_height, fill=True, stroke=False)

    path = pkg_resources.resource_filename(__name__, os.path.join('img',
      'unknown.jpg'))
    image = PIL.Image.open(path)

    image_height = 100
    image_width = (image_height/float(image.height)) * image.width
    padding = 0.5*cm
    image_x = page_width - image_width - padding
    image_y = page_height - padding - image_height
    border = 4
    canvas.setFillGray(1)
    canvas.setStrokeGray(0.8)
    canvas.roundRect(image_x-border, image_y-border, image_width + (2*border),
        image_height + (2*border), radius=border/2, fill=True, stroke=True)
    canvas.drawImage(path, image_x, image_y, width=image_width,
        height=image_height, mask=None)

    name = canvas.beginText()
    name.setTextOrigin(doc.leftMargin, y+0.4*cm)
    name.setFont('Times-Roman', 20)
    name.setFillGray(1)
    name.textLine(self.song.performer.name)
    canvas.drawText(name)

    revision = canvas.beginText()
    revision.setTextOrigin(doc.leftMargin, doc.bottomMargin-(0.1*cm))
    revision.setFont('Times-Italic', 9)
    revision.setFillColor(Color(0, 0.4, 0, 1))
    revision.textLine(self.song.modified.strftime(self.dateformat))
    canvas.drawText(revision)

    # draws a line between the columns if we are in two column mode
    if self.song.two_columns:
      start_pad = 1.5*cm
      canvas.setStrokeColor(self.performer_color())
      canvas.setLineWidth(0.1*cm)
      canvas.setStrokeAlpha(0.5)
      canvas.setLineCap(1) #round ends
      canvas.line(page_width/2, doc.bottomMargin+start_pad,
          page_width/2, image_y-border-start_pad)


  def template_id(self):
    return 'SongTemplate-%s' % self.song.slug


  def add_page_template(self, doc):
    """Adds song page template to the document."""

    from reportlab.lib.units import cm
    from reportlab.platypus.frames import Frame
    from reportlab.platypus.doctemplate import PageTemplate

    doc._calc() #taken from reportlab source code (magic)

    # The switch between one or two columns PDF output reflects on having one
    # or two frames. If we have two frames, the width and the start position
    # of each frame has to be computed slightly differently.
    #
    # Special attention to the right frame or its start will meet the picture
    # of the artist. So, we start about 2 cm down.

    if self.song.two_columns:

      padding = 0.5 * cm;
      frame_width = (doc.width - padding) / 2
      frames = [
          Frame(doc.leftMargin, doc.bottomMargin, frame_width, doc.height,
            id='column-1', leftPadding=0, rightPadding=0),
          Frame(doc.leftMargin + frame_width + padding, doc.bottomMargin,
            frame_width, doc.height - 2 * cm,
            id='column-2', leftPadding=0, rightPadding=0),
          ]
    else:
      frames = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
          id='normal', leftPadding=0, rightPadding=0)

    template = [PageTemplate(id='FirstPageSongTemplate', frames=frames,
      onPage=self.page_template_first, pagesize=doc.pagesize)]
    doc.addPageTemplates(template)
    template = [PageTemplate(id=self.template_id(), frames=frames,
      onPage=self.page_template, pagesize=doc.pagesize)]
    doc.addPageTemplates(template)


  def page_template_first(self, canvas, doc):
    """If the song is printed alone, the first page is special."""

    canvas.saveState()
    self.basic_page(canvas, doc)
    canvas.restoreState()


  def performer_color(self):
   """Returns the equivalent reportlab Color object from the artist color."""

   import struct
   from reportlab.lib.colors import Color

   rgb = struct.unpack('4B', struct.pack('>I', self.song.performer.color))[1:]
   pdf = [k/255.0 for k in rgb] + [1.0]
   return Color(*pdf)


  def page_template(self, canvas, doc):
    """Creates a personalized PDF page view for this song."""

    from reportlab.lib.units import cm

    canvas.saveState()

    self.basic_page(canvas, doc)

    # Draws song name and page number
    title = canvas.beginText()
    title.setTextOrigin(doc.leftMargin + doc.width/2, doc.bottomMargin-(0.1*cm))
    title.setFont('Times-Roman', 9)
    title.setFillGray(0.2)
    title.textLine(u"%s" % (self.song.title))
    page_x = doc.width+doc.rightMargin+0.2*cm
    page_y = doc.bottomMargin-(0.1*cm)
    page_fontsize = 11
    page = canvas.beginText()
    page.setTextOrigin(page_x, page_y)
    page.setFont('Helvetica-Bold', page_fontsize)
    page.setFillGray(1)
    page_number = doc.page
    page.textLine('%d' % page_number)

    #circle around number
    canvas.setFillColor(self.performer_color())
    circle_x, circle_y = page_circle_center(page_x, page_y,
        page_fontsize, page_number)
    canvas.circle(circle_x, circle_y, 1.5*page_fontsize, fill=True,
        stroke=False)

    canvas.drawText(title)
    canvas.drawText(page)

    canvas.restoreState()


  def story(self, doc):
    """Writes itself as a PDF story."""

    # what is the maximum width of text?
    if self.song.two_columns: width = colwidth['double']
    else: width = colwidth['single']

    story = [Paragraph(self.song.title, style['song-title'])]
    story.append(Paragraph('Tom: %s' % self.song.tone, style['tone']))
    story.append(Spacer(1, fontsize))
    story += [k.as_flowable(width) for k in self.song.items()]
    story = [k for k in story if k]

    return tide(story, doc)


@contextlib.contextmanager
def pelican_locale(settings):
  """Temporarily switches the locale to the top pelican one

  Parameters:

    settings (dict): Pelican settings

  """

  import locale

  # LOCALE setup
  # sets the locale so the dates and such get correctly printed
  pelican_locale = settings.get('LOCALE', ('en',))[0]

  old_locale = locale.getlocale()
  # this will try to get a language we support from the user preferences
  try_language = locale.normalize(pelican_locale)
  new_locale = (try_language, old_locale[1])
  try:
    locale.setlocale(locale.LC_ALL, new_locale)
  except:
    pass #we ignore problems setting the locale and leave the default

  yield

  # restore default language
  locale.setlocale(locale.LC_ALL, old_locale)


def chordbook(filename, objects, title, subtitle, url, settings):
  """Generate the PDF version of the chordbook


  Parameters:

    filename (str): The complete path to the destination filename

    objects (list): An ordered list of song objects that will be inserted into
      this chordbook

    title (str): The title that will be shown in italics. This is normally
      something like "Collection"

    subtitle (str): The subtitle. This is normally the name of the collection

    url (str): The URL to this PDF, so people can download it

    settings (dict): Pelican settings


  Returns:

    SongBookTemplate: A ReportLab BaseDocTemplate with all the songs encoded
    inside.

  """

  from reportlab.platypus.tableofcontents import TableOfContents
  from reportlab.platypus import NextPageTemplate, PageBreak

  with pelican_locale(settings):
    doc = SongBookTemplate(filename)
    siteurl = settings.get('SITEURL', 'http://example.com')
    doc.author = settings.get('AUTHOR', 'Unknown Editor')
    doc.title = 'Cifras de %s' % siteurl
    doc.subject = 'Compilação de Letras e Cifras'
    dateformat = settings.get('DEFAULT_DATE_FORMAT', '%d/%m/%Y')

    story = cover_page(title, subtitle, url, siteurl, dateformat)

    #appends and prepares table of contents
    story.append(NextPageTemplate('TOC'))
    story.append(PageBreak())
    story.append(TableOfContents())
    story[-1].levelStyles[0] = style['toc-entry']
    story[-1].dotsMinLevel = 0 #connecting dots

    #adds the lyrics
    for o in objects:
      po = PdfSong(o, dateformat)
      po.add_page_template(doc)
      story.append(NextPageTemplate(po.template_id()))
      story.append(PageBreak())
      story += po.story(doc)

    #multi-pass builds are necessary to handle TOCs correctly
    doc.multiBuild(story)

    return doc


def song(filename, song, settings):
  """Generate the PDF version of the chordbook


  Parameters:

    filename (str): The complete path to the destination filename

    song (Song): A single song object to create the PDF for
      this chordbook

    settings (dict): Pelican settings


  Returns:

    SongBookTemplate: A ReportLab BaseDocTemplate with the song encoded inside.

  """

  with pelican_locale(settings):

    doc = SongTemplate(filename)
    doc.author = settings.get('AUTHOR', 'Unknown Editor')
    doc.title = song.title
    doc.subject = 'Letra e Cifra'
    dateformat = settings.get('DEFAULT_DATE_FORMAT', '%d/%m/%Y')

    so = PdfSong(song, dateformat)

    story = so.story(doc)
    so.add_page_template(doc)
    doc.build(story)

    return doc

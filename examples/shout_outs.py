#!/usr/bin/python

# The MIT License
#
# Copyright (c) 2007 Damon Kohler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Record and display shout outs for the life of the server."""

import gsd

TEMPLATE = """
<html>
<head>
<title>Shout Outs!</title>
</head>
<body>
<form action="/" method="get">
<input name="shout">
<input type="submit" value="Shout!">
</form>
<?
for shout in self.shout_outs:
  print shout, '<br>'
?>
</body>
</html>
"""


class ShoutOuts(gsd.App):

  """A simple GSD app that records shout outs for the life of the server."""

  def __init__(self):
    self.shout_outs = []

  def GET_(self, shout=None):
    """Display shout outs and form to add new ones."""
    if shout is not None:
      self.shout_outs.append(shout[0])
    self.Render(TEMPLATE, locals())

  def GET_reset(self):
    """Reset the list of shoutouts."""
    self.shout_outs = []
    self.Redirect('/')


if __name__ == '__main__':
  app = ShoutOuts()
  print 'http://localhost:8000/'
  app.Serve('localhost', 8000)

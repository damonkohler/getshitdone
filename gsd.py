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

import BaseHTTPServer, cgi, os, re, SocketServer, StringIO, sys

TEMPLATE_TAGS = re.compile(r'(<\?)(.*?)\?>', re.DOTALL)


class Server(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
  pass


class App(BaseHTTPServer.BaseHTTPRequestHandler):

  """A self-serving web framework."""

  def __init__(self):
    pass

  def __call__(self, *args, **kwargs):
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    return self

  def _SendHeaders(self, response=200, key='Content-type', value='text/html'):
    self.send_response(response)
    self.send_header(key, value)
    self.end_headers()

  def _SendStaticFile(self, path):
    self._SendHeaders()
    self.wfile.write(open(path.replace('/', os.sep)).read())

  def Render(self, template, scope=None, response=200):
    """Render template with provided scope."""
    sys.stdout = StringIO.StringIO()
    parts = list(reversed(TEMPLATE_TAGS.split(template)))
    locals().update(scope or {})
    while parts:
      part = parts.pop()
      if part == '<?':
        exec parts.pop()
      else:
        print part
    self._SendHeaders(response)
    self.wfile.write(sys.stdout.getvalue())
    sys.stdout = sys.__stdout__

  def Redirect(self, path):
    self._SendHeaders(303, 'Location', path)

  def do_HEAD(self):
    self._SendHeaders()

  def do_POST(self):
    # TODO(damonkohler): Add POST support.
    self.Render('404 Error', response=404)

  def do_GET(self):
    if self.path.startswith('/static'):
      return self._SendStaticFile(self.path[1:])
    path, qs = (self.path.split('?', 1) + [''])[:2]
    path = path.replace('/', '_').replace('.', '_')
    try:
      handler = getattr(self, 'GET%s' % path)
    except AttributeError:
      self.Render('404 Error', response=404)
    else:
      handler(**cgi.parse_qs(qs))

  def Serve(self, host, port):
    try:
      Server((host, port), self).serve_forever()
    except KeyboardInterrupt:
      pass

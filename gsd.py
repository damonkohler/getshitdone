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

import BaseHTTPServer, cgi, os, re, SocketServer, StringIO, sys, traceback, socket

TEMPLATE_TAGS = re.compile(r'(<\?)(.*?)\?>', re.DOTALL)


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

  def __init__(self, app, *args, **kwargs):
    self.app = app
    self.logging_enabled = True
    try:
      BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    except socket.error, e:
      pass

  def log_request(self, *args, **kwargs):
    if self.logging_enabled:
      BaseHTTPServer.BaseHTTPRequestHandler.log_request(self, *args, **kwargs)

  def _SendHeaders(self, response=200, key='Content-type', value='text/html'):
    self.send_response(response)
    self.send_header(key, value)
    self.end_headers()

  def _SendStaticFile(self, path):
    self._SendHeaders()
    self.wfile.write(open(path.replace('/', os.sep), 'rb').read())

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
      get = getattr(self.app, 'GET%s' % path)
    except AttributeError, e:
      print '404 Error: %s' % e
      self.Render('404 Error', response=404)
    else:
      try:
        get(self, **cgi.parse_qs(qs))
      except:
        traceback.print_exc()
        sys.stderr.flush()

  def Render(self, template, scope=None, response=200):
    """Render template with provided scope."""
    out = StringIO.StringIO()
    parts = list(reversed(TEMPLATE_TAGS.split(template)))
    locals().update(scope or {})
    while parts:
      part = parts.pop()
      if part == '<?':
        exec parts.pop()
      else:
        out.write(part)
    self._SendHeaders(response)
    try:
      self.wfile.write(out.getvalue())
    except socket.error, e:
      pass

  def Redirect(self, path):
    self._SendHeaders(303, 'Location', path)


class App(object):

  """A self-serving web framework."""

  def Handler(self, *args, **kwargs):
    return RequestHandler(self, *args, **kwargs)

  def Serve(self, host, port):
    try:
      BaseHTTPServer.HTTPServer((host, port), self.Handler).serve_forever()
    except KeyboardInterrupt:
      pass

  def Main(self):
    if not len(sys.argv) > 2:
      print '%s host port' % __file__
      sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    print 'http://%s:%d/' % (host, port)
    self.Serve(host, port)

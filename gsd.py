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

import re
import BaseHTTPServer

TEMPLATE_TAGS = re.compile(r'(<\?)(.*?)\?>')


class App(BaseHTTPServer.BaseHTTPRequestHandler):

  """A self-serving web framework in under 50 lines of code."""

  def __call__(self, *args, **kwargs):
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    return self

  def _SendHeaders(self, response):
    self.send_response(response)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def Render(self, template_path, scope):
    """Render template from path with provided scope."""
    template = open(template_path).read()
    parts = TEMPLATE_TAGS.split(template)
    locals().update(scope)
    while parts:
      part = parts.pop()
      if part == '<?':
        exec parts.pop()
      else:
        self.wfile.write(part)

  def do_HEAD(self):
    self._SendHeaders(200)

  def do_POST(self):
    self._SendHeaders(404)

  def do_GET(self):
    path = self.path.split('?')[0]  # TODO(damonkohler): Parse GET params.
    path = self.path.replace('/', '_')
    path = path.replace('.', '_')
    try:
      handler = getattr(self, 'GET%s' % path)
    except AttributeError:
      self._SendHeaders(404)
    else:
      self._SendHeaders(200)
      handler()

  def Serve(self, host, port):
    try:
      BaseHTTPServer.HTTPServer((host, port), self).serve_forever()
    except KeyboardInterrupt:
      pass

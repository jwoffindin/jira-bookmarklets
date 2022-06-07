#!/usr/bin/env python

import glob
import yaml
import urllib
import jinja2

from markupsafe import Markup


class Bookmarklet:
  def __init__(self, content: str):
    config_line, _, body = content.partition("\n")

    config = yaml.safe_load(config_line)
    self.name = config["name"]
    self.template = config["template"]
    self.description = config["description"]

    template_file = f"templates/bookmarklet-{self.template}.j2"

    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    env.filters["urlencode"] = self.urlencode_filter
    template = env.from_string(open(template_file).read())

    self.url = template.render(content=body)

  def urlencode_filter(self, txt):
    if type(txt) == Markup:
      txt = txt.unescape()
    else:
      txt = txt.encode('ascii')

    return Markup(urllib.parse.quote_from_bytes(txt))

def main():
  bookmarklets = []
  for file in glob.glob("bookmarklets/*.txt"):
      bookmarklets.append(Bookmarklet(open(file).read()))

  with open("bookmarklets.html", "w") as fh:
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    template = env.from_string(
        open("templates/bookmarklets.html.j2").read())
    fh.write(template.render(bookmarklets=bookmarklets))

main()
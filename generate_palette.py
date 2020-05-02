#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inkscape extension to generate color palettes from selected objects' color properties
"""

import os
import sys
import inkex
import simplestyle

__version__ = '2.0'

inkex.localize()

def log(text):
  inkex.debug(text)

def abort(text):
  inkex.errormsg(_(text))
  exit()


class GeneratePalette(inkex.Effect):

  def __init__(self):
    inkex.Effect.__init__(self)

    self.OptionParser.add_option('-n', '--name', action='store', type='string', dest='name', help='Palette name')
    self.OptionParser.add_option('-p', '--property', action='store', type='string', dest='property', help='Color property')
    self.OptionParser.add_option('-d', '--default', action='store', type='inkbool', dest='default', help='Default grays')
    self.OptionParser.add_option('-r', '--replace', action='store', type='inkbool', dest='replace', help='Replace existing')

  def get_palettes_path(self):
    if sys.platform.startswith('win'):
      path = os.path.join(os.environ['APPDATA'], 'inkscape', 'palettes')
    else:
      path = os.environ.get('XDG_CONFIG_HOME', '~/.config')
      path = os.path.join(path, 'inkscape', 'palettes')

    return os.path.expanduser(path)

  def get_file_path(self):
    name = str(self.options.name).replace(' ', '-')
    return "%s/%s.gpl" % (self.palettes_path, name)

  def get_default_colors(self):
    colors = [
      "  0   0   0  Black",
      " 26  26  26  90% Gray",
      " 51  51  51  80% Gray",
      " 77  77  77  70% Gray",
      "102 102 102  60% Gray",
      "128 128 128  50% Gray",
      "153 153 153  40% Gray",
      "179 179 179  30% Gray",
      "204 204 204  20% Gray",
      "230 230 230  10% Gray",
      "236 236 236  7.5% Gray",
      "242 242 242  5% Gray",
      "249 249 249  2.5% Gray",
      "255 255 255  White"
    ]

    return colors if self.options.default else []

  def get_node_prop(self, node, property):
    style = simplestyle.parseStyle(node.attrib['style'])
    return style[property]

  def get_node_index(self, args):
    id, node = args
    return self.options.ids.index(id)

  def get_formatted_color(self, color):
    rgb = simplestyle.parseColor(color)
    rgb = "{:3d} {:3d} {:3d}".format(*rgb)

    return "%s  %s" % (rgb, color)

  def get_selected_colors(self):
    colors   = []
    selected = list(self.selected.items())

    selected.sort(key=self.get_node_index)

    for id, node in selected:
      if self.options.property in ['fill', 'both']:
        fill = self.get_node_prop(node, 'fill')

        if fill != 'none' and fill not in colors:
          colors.append(fill)

      if self.options.property in ['stroke', 'both']:
        stroke = self.get_node_prop(node, 'stroke')

        if stroke != 'none' and stroke not in colors:
          colors.append(stroke)

    return list(map(self.get_formatted_color, colors))

  def write_palette(self):
    file = open(self.file_path, 'w')

    try:
      file.write("GIMP Palette\n")
      file.write("Name: %s\n" % self.options.name)
      file.write("#\n# Generated with Inkscape Generate Palette\n#\n")

      for color in (self.default_colors + self.selected_colors):
        file.write("%s\n" % color)
    finally:
      file.close()

  def effect(self):
    self.palettes_path   = self.get_palettes_path()
    self.file_path       = self.get_file_path()
    self.default_colors  = self.get_default_colors()
    self.selected_colors = self.get_selected_colors()

    if not self.options.replace and os.path.exists(self.file_path):
      abort('Palette already exists!')

    if not self.options.name:
      abort('Please enter a palette name.')

    if len(self.options.ids) < 2:
      abort('Please select at least 2 objects.')

    if not len(self.selected_colors):
      abort('No colors found in selected objects!')

    self.write_palette()


if __name__ == '__main__':
  palette = GeneratePalette()
  palette.affect()

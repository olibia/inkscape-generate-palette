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

class GeneratePalette(inkex.Effect):

  def __init__(self):
    inkex.Effect.__init__(self)

    self.OptionParser.add_option('-n', '--name', action='store', type='string', dest='name', help='Palette name')
    self.OptionParser.add_option('-p', '--property', action='store', type='string', dest='property', help='Color property')
    self.OptionParser.add_option('-d', '--default', action='store', type='string', dest='default', help='Default grays')
    self.OptionParser.add_option('-r', '--replace', action='store', type='string', dest='replace', help='Replace existing')

  def palettes_path(self):
    if sys.platform.startswith('win'):
      path = os.path.join(os.environ['APPDATA'], 'inkscape', 'palettes')
    else:
      path = os.environ.get('XDG_CONFIG_HOME', '~/.config')
      path = os.path.join(path, 'inkscape', 'palettes')

    return os.path.expanduser(path)

  def file_path(self):
    name = self.options.name.replace(' ', '-')
    path = self.palettes_path()
    path = "%s/%s.gpl" % (path, name)

    if self.options.replace == 'false' and os.path.exists(path):
      inkex.errormsg(_('Palette already exists!'))
      exit()

    return path

  def hex_to_rgb(self, color):
    rgb = list(map(lambda s: int(s, 16), (color[1:3], color[3:5], color[5:7])))
    return rgb

  def default_colors(self):
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

    return "\n".join(colors)

  def get_node_styles(self, node):
    return simplestyle.parseStyle(node.attrib['style'])

  def get_color_values(self):
    colors   = []
    selected = self.selected.items()

    selected.sort(key=lambda n: '{0:0>8}'.format(n[0]))

    for id, node in selected:
      if self.options.property in ['fill', 'both']:
        fill = self.get_node_styles(node)['fill']
        if fill != 'none': colors.append(fill)

      if self.options.property in ['stroke', 'both']:
        stroke = self.get_node_styles(node)['stroke']
        if stroke != 'none': colors.append(stroke)

    return colors

  def write_palette(self):
    colors = self.get_color_values()

    if len(colors) == 0:
      inkex.errormsg(_('No colors found in selected objects!'))
      exit()

    file = open(self.file_path(), 'w')
    file.write("GIMP Palette\n")
    file.write("Name: %s\n" % self.options.name)
    file.write("#\n# Generated with Inkscape Generate Palette\n#\n")

    if self.options.default == 'true':
      file.write("%s\n" % self.default_colors())

    for color in colors:
      rgb = self.hex_to_rgb(color)
      file.write("%s  %s\n" % ("{:3d} {:3d} {:3d}".format(*rgb), color))

  def effect(self):
    if self.options.name is None:
      inkex.errormsg(_('Please enter a palette name.'))
      exit()

    if len(self.options.ids) < 2:
      inkex.errormsg(_('Please select at least 2 objects.'))
      exit()

    self.write_palette()


if __name__ == '__main__':
  palette = GeneratePalette()
  palette.affect()

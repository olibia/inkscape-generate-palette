# Inkscape Generate Palette
Inkscape extension to generate color palettes from selected objects' color properties.

![Screenshot](https://raw.githubusercontent.com/olibia/inkscape-generate-palette/master/screenshot.png)

## Install

#### Inkscape Extensions
Download from Inkscape's Extensions page [here](https://inkscape.org/en/~olibia/%E2%98%85generate-palette-extension).

#### Arch Linux
[AUR package](https://aur.archlinux.org/packages/inkscape-generate-palette)

### Manual installation

#### Linux
Copy extension files `generate_palette.inx` and `generate_palette.py` into `~/.config/inkscape/extensions`.

#### Windows
Copy extension files `generate_palette.inx` and `generate_palette.py` into the path shown in Inkscape preferences.
See Edit > Preferences > System: User extensions.

## Usage
* Create objects with color properties set, can be fill and/or stroke color.
* Select them and from the Extensions menu choose Palette and Generate.
* Provide a name and select the color property to grab colors from.

*You can also include Inkscape's default black to white colors or replace an existing palette.*

### Notes
* Inkscape needs to be restarted for the extension to appear.
* `python2-lxml` must be installed for this extension to work.
* Inkscape must be restarted for a new palette to appear.
* Generated palettes are located at `~/.config/inkscape/palettes` or `~\AppData\Roaming\inkscape\palettes` on Windows.

## License
[GPLv3](http://www.gnu.org/licenses/gpl-3.0.en.html)

import os
import re

from cairosvg import svg2png

def convertSVG2PNG(svg_name):
    # Components and file paths
    svg_components_path = './' + svg_name + '/components_svg'
    png_components_path = './' + svg_name + '/components_png'

    # Load svg components
    files = os.listdir(svg_components_path)
    svg_files =list(filter(lambda name: re.match('.*\.svg', name), files))

    # Make sure that folder were png components will be stored is empty
    files = os.listdir(png_components_path)
    for file in files:
        os.remove(png_components_path + '/' + file)

    # Save png components
    for svg in svg_files:
        svg2png(url = svg_components_path + '/' + svg,
            background_color = 'white',
            write_to = png_components_path + '/' + svg[:-3] + 'png')

    print('Components from ' + svg_name + ' transformed with success!')
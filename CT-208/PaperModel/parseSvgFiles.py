import re
import os
import xml.etree.ElementTree as ET

from utils           import translatePath
from svgpathtools    import svg2paths2, wsvg, parse_path, Arc


def parseSVG(svg_name):
    """
    This script reads a .svg and processess it to output separated .svg files.
    """
    # Components and file paths
    svg_components_path = './' + svg_name + '/components_svg'
    svg_file_path = './' + svg_name + '/' + svg_name + '.svg'

    # Make sure that folder were svg components will be stored is empty
    files = os.listdir(svg_components_path)
    for file in files:
        os.remove(svg_components_path + '/' + file)

    # Open figure into svgFile and read into svgString
    svgFile = open(svg_file_path,'r')
    svgString = svgFile.read()
    svgFile.close()

    # Remove section <defs> ... </defs> from svgString because it is not useful
    svgString = re.sub('<defs.*>.*</defs>','<defs/>',svgString, flags=re.DOTALL)
    svg_file_path = './' + svg_name + '/' + svg_name + '_processed' + '.svg'
    newSvgFile = open(svg_file_path,'w')
    newSvgFile.write(svgString)

    # Reads .svg as a tree element
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    g_path_qty = []

    # finds the final g tag elements and the qty of paths in each one
    # this enumerator will be useful when working with svgpathtools
    for g_tag in root.findall('.//{http://www.w3.org/2000/svg}g'):
        path_qty = len(g_tag.findall('{http://www.w3.org/2000/svg}path'))
        if path_qty > 0:
            g_path_qty.append(path_qty)

    # Reads the svg with svgpathtools
    paths, attributes, svg_attributes = svg2paths2(svg_file_path)
    # Figure line stroke width of 5mm to guarantee the distance
    # Extract height and width params
    width_mm = float(svg_attributes['width'][:-2])
    height_mm = float(svg_attributes['height'][:-2])
    _, _, width_px, height_px = svg_attributes['viewBox'].split(" ")
    width_px = float(width_px)
    height_px = float(height_px)

    MM2PX = width_px / width_mm
    PX2MM = width_mm / width_px
    strokeWidth = MM2PX * 5

    # Increases path line width to be 5mm, rounds linecaps, rounds linejoints, fills components with black
    for attribute in attributes:
        # increases path line width to be 5mm
        try:
            attribute['style'] = re.sub('stroke-width:[0-9.]*', 'stroke-width:' + str(strokeWidth), attribute['style'])
        except:
            pass
        # rounds linecaps
        try:
            attribute['style'] = re.sub('stroke-linecap:[a-z]*', 'stroke-linecap:round', attribute['style'])
        except:
            pass
        # rounds linejoints
        try:
            attribute['style'] = re.sub('stroke-linejoin:[a-z]*', 'stroke-linejoin:round', attribute['style'])
        except:
            pass
        # removes linemiter limits because they do not make sense in round joints
        try:
            attribute['style'] = re.sub(';stroke-miterlimit:[0-9.]*;', ';', attribute['style'])
        except:
            pass
        # fills with black
        try:
            attribute['style'] = re.sub('fill:[0-9a-z.#]*', 'fill:black', attribute['style'])
        except:
            pass

    # removes transform attributes and includes it on path tag lines
    for i in range(0,len(paths)):
        try:
            translation = attributes[i].pop('transform')
            translation = translation[translation.find('(') + 1: translation.find(')')].split(',')
            paths[i] = parse_path(translatePath(paths[i].d(), float(translation[0]), float(translation[1])))
        except:
            continue

    # separates components
    components = []
    for idx, qty in enumerate(g_path_qty):
        components.append([paths[0:qty], attributes[0:qty], svg_attributes])
        paths = paths[qty:]
        attributes = attributes[qty:]

    # moves components to the superior left corner of svg and adjust viewbox
    for idx, component in enumerate(components):
        # component[h]: paths if h=0; attributes if h=1, svg_attributes if h=2
        # component[0][p] is the component path
        # component[0][p][l] is the line "l" of path "p"
        # component[0][p][l][d] is the point "d" of line "l"
        x_min = 50000
        y_min = 50000
        x_max = -50000
        y_max = -50000
        # gets the min and max x and y in component 
        for path in component[0]:
            for line in path:
                if type(line) != Arc:
                    for dot in line:
                        if dot.real < x_min: x_min = dot.real
                        if dot.real > x_max: x_max = dot.real
                        if dot.imag < y_min: y_min = dot.imag
                        if dot.imag > y_max: y_max = dot.imag

        # translates position so that it fits in square(0,0,X,Y)
        translation = [-x_min + strokeWidth/2, -y_min + strokeWidth/2]
        for path_idx in range(0, len(component[0])):
            #for i in range(0,len(paths)):
            try:
                component[0][path_idx] = parse_path(translatePath(component[0][path_idx].d(), float(translation[0]), float(translation[1])))
            except:
                continue
    
        # changes the viewBox and the size(in "mm") of svg
        comp_width_px = x_max + strokeWidth - x_min
        comp_height_px = y_max + strokeWidth - y_min
        components[idx][2]['width'] = comp_width_px * PX2MM 
        components[idx][2]['height'] = comp_height_px * PX2MM 
        components[idx][2]['viewBox'] = ' '.join(map(str,[0,0,comp_width_px,comp_height_px])) 
        # if this step be performed outside the loop it does not work this is the only reason 
        wsvg(paths = components[idx][0], attributes = components[idx][1], 
            svg_attributes=components[idx][2], 
                filename=svg_components_path + "/" + str(idx).zfill(3) + '.svg')

    print('Components from ' + svg_name + ' separated with success!')
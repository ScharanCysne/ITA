import os
import re
import pickle
import numpy as np

from cairosvg               import svg2pdf
from svgpathtools           import svg2paths2, svg2paths
from svgpathtools.paths2svg import wsvg

def convertPNG2SVG(svg_name):
    # Components and file paths
    svg_components_path = './' + svg_name + '/components_svg'
    opt_results_path = './' + svg_name + '/results.pkl'
    results_path = './' + svg_name + '/results'

    files = os.listdir(svg_components_path)
    files = list(filter(lambda name: re.match(name[-3:],'svg'), files))

    # Change filling and stroke width attributes
    for file in files:
        paths, attributes, svg_attributes = svg2paths2(svg_components_path + '/' + file)
        for attribute in attributes:
            try: attribute['stroke-width'] = '1'
            except: continue
        for attribute in attributes:
            try: attribute['fill'] = 'none'
            except: continue
        for attribute in attributes:
            try: attribute['style'] = re.sub('fill:black','fill:none',attribute['style'])
            except: continue
        for attribute in attributes:
            try: attribute['style'] = re.sub('stroke-width:[0-9.]*','stroke-width:1',attribute['style'])
            except: continue
        wsvg(paths=paths, attributes=attributes, svg_attributes = svg_attributes, filename=svg_components_path + '/' + file)
        
    # open the results from optimization
    with open(opt_results_path, 'rb') as input:
        results = pickle.load(input)

    # get svg general attributes from original svg
    MM2PX = float(svg_attributes['viewBox'].split()[2]) / float(svg_attributes['width'][:-2])
    _, _, svg_attributes = svg2paths2(svg_name + "/" + svg_name + '.svg')

    # Update svg height, length and viewBox attributes to page size
    height, width = np.shape(results[0].__getattribute__('page'))
    svg_attributes['width'] = str(width) + 'mm'
    svg_attributes['height'] = str(height) + 'mm'
    svg_attributes['viewBox'] = ' '.join(map(str,[0, 0, width*MM2PX, height*MM2PX]))

    # includes translation results in the svgs
    pages = [[[],[]]]
    for component in results:
        # chekc page transition - create new page if necessary
        if component.__getattribute__('page_idx') + 1 > len(pages):
            pages.append([[],[]])

        paths, attributes = svg2paths(svg_components_path + '/' + component.__getattribute__('name')[:-3] + 'svg')
        positionY, positionX, angle = component.__getattribute__('placedPosition')
        componentLength = component.__getattribute__('componentLength')
        componentHeight = component.__getattribute__('componentHeight')

        for attribute in attributes:
            if angle == 1:
                attribute['transform'] = 'translate(' + str(positionX * MM2PX) + ',' + str((positionY - componentHeight) * MM2PX) + ') rotate(90)'
            elif angle == -1:
                attribute['transform'] = 'translate(' + str(positionX * MM2PX) + ',' + str(positionY * MM2PX) + ') rotate(-90)'
            else:
                attribute['transform'] = 'translate(' + str(positionX * MM2PX) + ',' + str(positionY * MM2PX) + ')'

        while paths:
            pages[-1][0].append(paths.pop(0))
            pages[-1][1].append(attributes.pop(0))

    for idx, page in enumerate(pages):
        wsvg(paths=page[0], attributes=page[1], svg_attributes=svg_attributes, filename=results_path + '/page' + str(idx).zfill(2) + '.svg')

    files = os.listdir(results_path)
    files = list(filter(lambda name: re.match(name[-3:],'svg'), files))

    for file in files:
        svg2pdf(url=results_path + '/' + file, write_to=results_path + '/' + file[:-3] + 'pdf')

    print('Success! See results in folder /' + svg_name + '/results/')
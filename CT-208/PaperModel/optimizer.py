import os
import re
import numpy as np

from PIL             import Image
from utils           import binarray2jpg, png2bin, selectComponentToPlace
from placeComponent  import ComponentPlacing

print('Optimizing position in page...')

# Select figure in folder
#params = {'name':'example', 'MM2PX': 1, 'PX2MM': 1}
params = {'name':'harry-potter', 'MM2PX': 3.7795276032851057, 'PX2MM': 0.2645833302370423}
#params = {'name':'e190-e2', 'MM2PX': 1, 'PX2MM': 1}

# Get parameters
svg_name = params['name']
MM2PX = params['MM2PX']
PX2MM = params['PX2MM']

# Sheet size
PAGE_SIZE = (210,297) 

# Components and file paths
png_components_path = './' + svg_name + '/components_png'
test_results_path = './' + svg_name + '/test_results'
opt_results_path = './' + svg_name + '/results.pkl'

# Finds the component png file in the directory
files = os.listdir(png_components_path)
pngs = list(filter(lambda name: re.match('.*\.png', name), files))

# Creates a list of pages and append a page of (height, lenght) px
pages = []
pages.append(np.zeros(PAGE_SIZE, dtype=int))
# Transforms each png component into a binary matrix
# List of binary matrix of components and its name
components = [[png2bin(png_components_path+ '/' + png), png] for png in pngs] 
# Creates a list of objects of class ComponentPlacing
CP_list = [ComponentPlacing(pages[0], component, num_iterations=300) for component in components]

# Place components on page
Results = []
page_idx = 0
max_attempts = 100
num_components = len(CP_list)

while CP_list:
    attempt = 0     # counter of times that try to fit component in a page
    # This loop tries to fit a component on current page    
    while attempt < max_attempts:
        # Selects one aleatory component
        idx = selectComponentToPlace(CP_list)
        CP_object = CP_list[idx]
        # Finds the best position
        CP_object.FindCandidatePosition()
        # Checks if there is no intersection and place the compoponent if not
        if CP_object.NoIntersection():
            pages[page_idx] = CP_object.PlaceComponentInPage()
            # removes the placed component from the list and store in results list
            Results.append(CP_list.pop(idx)) 
            num_components -= 1
            print(('Current page: ' + str(page_idx+1)).ljust(18) + 'Components remaining: ' + str(num_components)+'...')
            
            if CP_list: 
                attempt = 0
            else: 
                break
        else: 
            attempt += 1
            CP_object.resetParameters() # sorts a new initial point
            
    # Prepares a new page if necessary
    if CP_list:
        pages.append(np.zeros(PAGE_SIZE, dtype=int))
        page_idx += 1
        for CP_object in CP_list:
            # sorts new initial point for the objects
            CP_object.page = pages[page_idx]
            CP_object.page_idx = page_idx
            CP_object.resetParameters()

# Remove all png files from the folder before storing the results
files = os.listdir(test_results_path)
for file in files:
    os.remove(test_results_path + '/' + file)

# Saves pages
for idx,page in enumerate(pages):
    image = binarray2jpg(page).astype(np.uint8)
    image = Image.fromarray(image)
    image.save(test_results_path + '/page' + str(idx).zfill(2) + '.png')

print('Finished optimization.')
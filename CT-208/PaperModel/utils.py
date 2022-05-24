import re
import pickle
import numpy as np

from PIL import Image

def translatePath (path, x, y):
    parse = re.split('[ ,]',path)
    string =''
    while parse:
        elem = parse.pop(0)
        if re.match('[A-Za-z]',elem):
            string += elem + ' '
        else:
            string += str(float(elem) + x) + ','
            string += str(float(parse.pop(0)) + y)
        if parse:
            string += ' '
    return string


def jpg2binarray(imgarray):
    """input: jpeg array
    output: int array, 0 is white px and 1 is black px"""
    imgreturn = imgarray[:,:,0]
    for i in range(0,np.shape(imgarray)[0]):
        for j in range(0,np.shape(imgarray)[1]):
            if imgreturn[i,j] > 10:
                imgreturn[i,j] = 0
            else:
                imgreturn[i,j] = 1
    return imgreturn


def binarray2jpg(binarray):
    imgarray = np.zeros([np.shape(binarray)[0],np.shape(binarray)[1],3])
    for i in range(0,np.shape(imgarray)[0]):
        for j in range(0,np.shape(imgarray)[1]):
            for k in range(0,np.shape(imgarray)[2]):
                if binarray[i,j]==1:
                    imgarray[i,j,k] = 0
                else:
                    imgarray[i,j,k] = 255
    return imgarray


def png2bin(png):
    image = Image.open(png)
    image = np.array(image)
    image = jpg2binarray(image)
    return image


def rotateBinaryImage (image, ang):
    im_height = np.shape(image)[0]
    im_width = np.shape(image)[1]
    max_dim = max([im_height, im_width])
    surface = np.zeros(np.array([2*max_dim,2*max_dim]))
    ang = ang * np.pi/180
    rotPoint = np.array([max_dim,max_dim], dtype = int)
    for y in range(0, im_height):
        for x in range(0, im_width):
            if image[y,x]:
                yl = y - int(im_height/2)
                xl = x - int(im_width/2)
                surface_y = int(max_dim + np.sin(ang)*xl + np.cos(ang)*yl)
                surface_x = int(max_dim + np.cos(ang)*xl - np.sin(ang)*yl)
                surface[surface_y:surface_y + 2, surface_x: surface_x +2] = np.ones([2,2], dtype = int)

    # removes blank lines and blank columns and update rotation point
    i = 0
    while not np.sum(surface[i]):
        i += 1
    surface = surface[i:]
    rotPoint[0] -= i
    i = 0
    while i < np.shape(surface)[0]:    
        if not np.sum(surface[i]):
            surface = np.delete(surface, i, axis = 0)
        else: i += 1
    i = 0
    while not np.sum(surface[:,i]):
        i += 1
    surface = surface[:,i:]
    rotPoint[1] -= i
    i = 0
    while i < np.shape(surface)[1]:    
        if not np.sum(surface[:,i]):
            surface = np.delete(surface, i, axis = 1)
        else: i += 1
    
    return surface, rotPoint


def clamp(value, minimum, maximum):
    """
    Clamps a value to keep it within the interval [minimum, maximum].

    :param value: value to be clamped.
    :type value: float.
    :param minimum: minimum value.
    :type minimum: float.
    :param maximum: maximum value.
    :type maximum: float.
    :return: clamped value.
    :rtype: float.
    """
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    return value


def selectComponentToPlace(compList):
    # selects the bigger component with prob 15%, otherwise, selects random
    if np.random.uniform() < 0.15:
        return max(range(len(compList)), key = lambda idx: compList[idx].__getattribute__('area'))
    else:
        return np.random.randint(len(compList))


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

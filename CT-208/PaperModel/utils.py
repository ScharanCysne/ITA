import re
import pickle
import numpy as np
import warnings

from PIL import Image

warnings.filterwarnings("ignore")

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


def clamp(value, minimum, maximum):
    """
    Clamps a value to keep it within the interval [minimum, maximum].
    """
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    return value


def selectComponentToPlace(compList):
    # selects the bigger component with prob 20%, otherwise, selects random
    if np.random.uniform() < 0.5:
        return max(range(len(compList)), key = lambda idx: compList[idx].__getattribute__('area'))
    else:
        return np.random.randint(len(compList))

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
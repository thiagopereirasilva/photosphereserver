from PIL import Image
from zipfile import ZipFile
import numpy as np
import sys
import getopt
import glob
import piexif
import os
import werkzeug
import jsonpickle
import cv2
import base64

#docker run -d -p 27017:27017 -p 28017:28017 mongo

print('[Info]\t\tCalibrating the following images')
path = os.getcwd()
path = path + '/download/' + uuid_code
 # if (os.path.isdir(path) == False):
 # dispara exception

 imagens = procurar_imagens(path)
  stringaa = ''
   for img in imagens:
        stringaa += " " + img
    print(stringaa)

    corrigir_imagens(imagens, path)

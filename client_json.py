from __future__ import print_function
import numpy as np
from PIL import Image
import requests
import json

addr = 'http://localhost:5000'
URL = addr + '/test'
image_name = 'image.jpg'

# prepare headers for http request
content_type = 'application/json'
headers = {'content-type': content_type,
           'label': 'myLabel.jpg',
           'description': 'myDescription',
           'date': 'myDate',
           'calibration': 'myCalibration',
           'author': 'myAuthor'}

image = Image.open(image_name)
json_data = json.dumps(np.array(image).tolist())
data = {'image': json_data}
#print (json.dumps(json_data))

response = requests.post(URL, data=data, headers=headers)
print(json.loads(response.text))

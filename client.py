from __future__ import print_function
import requests
import json
import uuid
import cv2
from datetime import date

addr = 'http://localhost:5000'
test_url = addr + '/images/upload'
image_name = 'image_teste.jpg'
uuid_code = str(uuid.uuid1())
myDescription = 'Photo description'
today = str(date.today())
author = 'Thiago Silva'
counter = 1
for x in range(7):

    # prepare headers for http request
    content_type = 'image/jpeg'

    headers = {'content-type': content_type,
               'phone_img_name': uuid_code + "_" + str(counter) + ".jpg",
               'phone_UUID': uuid_code,
               'phone_description': myDescription,
               'phone_date': today,
               'phone_calibration': 'myCalibration',
               'phone_author': author}
    counter += 1
    img = cv2.imread(image_name)
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    response = requests.post(
        test_url, data=img_encoded.tostring(), headers=headers)
    # decode response
    print(json.loads(response.text))
    
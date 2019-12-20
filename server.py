from flask import Flask, request, Response, url_for, send_file, send_from_directory, safe_join, abort
from flask_pymongo import PyMongo
from PIL import Image
from zipfile import ZipFile
import numpy as np
import pymongo
import sys
import getopt
import glob
import piexif
import os
import werkzeug
import jsonpickle
import cv2
import base64
import datetime
import time

# Initialize the Flask application
app = Flask(__name__)
app.config["CLIENT_IMAGES"] = "/home/thiago/Desktop/Workspace/PhotoSphere/download"

# Initialize Mongo connector
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["photosphere"]


def procurar_imagens(pasta_fonte='./download'):
    # arquivos = os.listdir(pasta_fonte)
    arquivos = glob.glob(os.path.join(pasta_fonte, '*.jpeg'))

    if arquivos:
        for arquivo in arquivos:
            if (arquivo.endswith(".jpeg") != True):
                arquivos.remove(arquivo)
    else:
        print('[Alerta]\tNenhum arquivo JPEG encontrado em "{0}"!'.format(
            pasta_fonte))
    return arquivos


def corrigir_imagens(imagens, pasta_destino=''):
    for imagem in imagens:
        try:
            img = Image.open(imagem)
        except Exception:
            print('[Erro]\t\tImpossivel ler o arquivo "{0}"'.format(imagem))
            sys.exit(2)

        exif_dict = piexif.load(imagem)
        # exif_dict = piexif.load(img.info["exif"])
        # exif_dict = img._getexif() //nao funciona
        # print('[Info]\t\tEXIF')
        # print(exif_dict)

        arquivo = os.path.basename(imagem)

        try:
            print('[Info]\t\tAdding EXIF in "{0}"'.
                  format(arquivo))
            exif_dict['Exif'][piexif.ExifIFD.FNumber] = (71, 10)
        except Exception:
            print('[Erro]\t\tError ao tentar adicionar informacao no arquivo "{0}"'.
                  format(imagem))
            sys.exit(2)

        exif_bytes = piexif.dump(exif_dict)

        if not os.path.exists(pasta_destino):
            os.mkdir(pasta_destino)

        nova_imagem = os.path.join(pasta_destino, arquivo)

        print('[Info]\t\tSalving file "{0}"'.
              format(nova_imagem))

        img.save(nova_imagem, "jpeg", exif=exif_bytes)


@app.route('/images/hdr/<uuid_code>/<calibration>', methods=['GET'])
def generate_hdr(uuid_code, calibration):
    print('[Info]\tCalibrating the following images')
    path = os.getcwd()
    path = path + '/download/' + uuid_code

    imagens = procurar_imagens(path)
    images_path = ''
    for img in imagens:
        images_path += " " + img

    corrigir_imagens(imagens, path)

    print('[Info]\tRunning hdrgen')
    # call hdrgen
    # hdr_path = "/download/" + uuid_code + "/" + uuid_code + "_output.jpg"
    os.popen('./hdrgen/hdrgen -o ' + "/download/" + uuid_code +
             "/" + uuid_code + "_output.jpg" + " " + images_path)

    return send_file("teste.jpg", mimetype="image/gif")


@app.route('/images/upload', methods=['POST'])
def upload():
    print("[Info]\tReceived a request")
    file_name = ''
    uuid_code = ''

    # get current directory
    path = os.getcwd()
    if 'phone_img_name' in request.headers:
        file_name = request.headers.get('phone_img_name')
        uuid_code = request.headers.get('phone_UUID')

    # nparr = np.fromstring(request.data, np.uint8)
    # decode image
    array_img = base64.b64decode(request.data)

    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    path = path + '/download/' + uuid_code
    if (os.path.isdir(path) == False):
        os.mkdir(path)
    print("[Info]\t\tSaving image <" + file_name + "> belongs to ImageSet <" +
          uuid_code + "> \n on directory \n" + path)

    # cv2.imwrite(path +'/'+file_name, img)
    with open(path+'/'+file_name, 'wb') as f_output:
        f_output.write(array_img)

    response = {'message': 'created'}
    print("[Info]\t\tSend response: " + str(response))
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=201, mimetype="application/json")


# docker run -d -p 27017:27017 -p 28017:28017 mongo
@app.route('/imageset', methods=['POST'])
def create_imageset():
    print("[Info]\tSalving imageSet")
    content = request.json
    uid = content['uuid']

    # getting images paths
    path = os.getcwd()
    path = path + '/download/' + uid
    images_path = procurar_imagens(path)
    images_path_str = []
    for img in images_path:
        # images_path_str.append(img)
        arr = img.split("/")
        images_path_str.append(arr[len(arr)-1])

    # getting actual time (long format)
    actual_time = int(round(time.time()*1000))

    doc = {'_id': uid, 'uuid': uid, 'label': content['label'],
           'description': content['description'],
           'author': content['author'], 'created_date': actual_time}
    doc['images_paths'] = images_path_str

    customers = db["imageset"]
    ids = customers.insert(doc)
    print('[Info]\t\tImageset ' + str(ids) + ' created')
    resp = {'message': 'Imageset ' + str(ids)+' created'}
    response_pickled = jsonpickle.encode(resp)

    return Response(response=response_pickled, status=201, mimetype="application/json")


@app.route('/imageset', methods=['GET'])
def getAllImageSet():
    print("[Info]\t\tGetting all imageSet")
    all_imageset = []
    customers = db["imageset"]
    for x in customers.find():
        dd = x['created_date']
        x['created_date'] = str(dd)
        pathService = []
        for path in x['images_paths']:
            # print(path)
            path = "http://10.7.128.18:5000/images/" + x['_id'] + "/" + path
            # path = url_for('/images/' + x['_id'] + "/" + path)
            # path = url_for('uploadTest')
            pathService.append(path)

        x['images_paths'] = pathService

        all_imageset.append(x)

    # print(all_imageset)
    response_pickled = jsonpickle.encode(all_imageset)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/images/<uuid_code>/<image>', methods=['GET'])
def uploadTest(uuid_code, image):
    print("[Info]\t\tSending image")
    image_path = "download/"+uuid_code+"/"+image
    return send_file(image_path, mimetype='image/jpg')


# @app.route("/image/<image_name>", methods=['GET'])
# def get_image(image_name):
#     try:
#         return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
#     except:
#         abort(404)


# start flask app
app.run(host="0.0.0.0", port=5000)

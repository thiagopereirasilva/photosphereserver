from flask import Flask, request, Response, url_for, send_file
from flask_pymongo import PyMongo
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

# Initialize the Flask application
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo = PyMongo(app)


def procurar_imagens(pasta_fonte='./download'):
    # arquivos = os.listdir(pasta_fonte)
    arquivos = glob.glob(os.path.join(pasta_fonte, '*.jpeg'))

    if arquivos:
        for arquivo in arquivos:
            if (arquivo.endswith(".jpg") != True):
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


@app.route('/images/hdr', methods=['GET'])
def calibrate():
    uuid_code = '408dd860-b363-489f-8f53-b8fae89a312f'
    luminance = '50'
    error_msg = ''

    if 'phone_UUID' in request.headers:
        uuid_code = request.headers.get('phone_UUID')
    else:
        error_msg = "Cannot generate HDR. No UUID has been specified."

    if 'luminance_factor' in request.headers:
        luminance = request.headers.get('luminance_factor')
    else:
        error_msg = "Cannot generate HDR. No luminance value has been specified."

    # If not luminance or uuid
    # if error_msg:
    #     print('[Error]\t\t' + error_msg)
    #     resp = {'message': error_msg
    #             }
    #     return Response(response=jsonpickle.encode(resp), status=500, mimetype="application/json")

    print('[Info]\tCalibrating the following images')
    path = os.getcwd()
    path = path + '/download/' + uuid_code
    # if (os.path.isdir(path) == False):
    # throw exception

    imagens = procurar_imagens(path)
    images_path = ''
    for img in imagens:
        images_path += " " + img

    corrigir_imagens(imagens, path)

    print('[Info]\tRunning hdrgen')
    # call hdrgen
    os.popen('./hdrgen/hdrgen -o ' + "/download/" + uuid_code +
             "/" + uuid_code + "_output.jpg " + images_path)

    # send response
    resp = {'message': 'Ok. HDR gerado'
            }
    response_pickled = jsonpickle.encode(resp)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/images/upload', methods=['POST'])
def upload():
    print("Received a request")
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
    print("Saving image <" + file_name + "> belongs to ImageSet <" +
          uuid_code + "> \n on directory \n" + path)

    # cv2.imwrite(path +'/'+file_name, img)
    with open(path+'/'+file_name, 'wb') as f_output:
        f_output.write(array_img)

    # build a response dict to send back to client
    # response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),
     #           'size': img.size,
      #          'nbytes': img.nbytes,
        #         }
    response = {'message': 'cabeca de tecao'}
    print("Send response: " + str(response))
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/images/get_hdr', methods=['GET'])
def uploadTest():
    print("Testing image send")
    filename = 'teste.jpg'
    return send_file(filename, mimetype='image/jpeg', attachment_filename="ronaldo")


@app.route('/images/save', methods=['GET'])
def save():
    print("salvando no banco")
    img = cv2.imread("teste.jpg")
    mongo.save_file("arquivo_thiago", img)
    mongo.db.users.insert({'username': 'Thiago', 'arquivo': img})

    # content_type = 'image/jpeg'
    # image_name = 'teste.jpg'
    # headers = {'content-type': content_type,
    #            'phone_description': 'Flamengo vai levar peia!'
    #            }
    # img = cv2.imread(image_name)
    # _, img_encoded = cv2.imencode('.jpg', img)

    # return Response(data=img_encoded, status=200, mimetype="image/jpeg")


# start flask app

app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, Response
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


def procurar_imagens(pasta_fonte='./download'):
    #arquivos = os.listdir(pasta_fonte)
    arquivos = glob.glob(os.path.join(pasta_fonte, '*.jpg'))

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
        #exif_dict = piexif.load(img.info["exif"])
        # exif_dict = img._getexif() //nao funciona
        print('[Info]\t\tEXIF')
        print(exif_dict)

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


# Initialize the Flask application
app = Flask(__name__)

""" @app.route('/test', methods=['POST'])
def test():
    print("Received a image inside a json message")
    print()
    resp = {'message': 'Ok'
            }
    response_pickled = jsonpickle.encode(resp)
    return Response(response=response_pickled, status=200, mimetype="application/json")
 """


@app.route('/images/hdr', methods=['GET'])
def calibrate():
    uuid_code = ''
    if 'phone_UUID' in request.headers:
            uuid_code = request.headers.get('phone_UUID')

    print('[Info]\t\tCalibrating the following images')
    path = os.getcwd()
    path = path + '/download/' + uuid_code
    #if (os.path.isdir(path) == False):
         #dispara exception  

    imagens = procurar_imagens(path)
    #for img in imagens:
     #   print("[Info]\t\t\t"+img)

    corrigir_imagens(imagens, path)
    resp = {'message': 'Ok'
            }
    response_pickled = jsonpickle.encode(resp)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/images/upload', methods=['POST'])
def upload():
    print("Received a request")
    file_name = ''
    uuid_code = ''
    #current directory
    path = os.getcwd()
    if 'phone_img_name' in request.headers:
        file_name = request.headers.get('phone_img_name')
        uuid_code = request.headers.get('phone_UUID')

    nparr = np.fromstring(request.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    path = path + '/download/' + uuid_code
    if (os.path.isdir(path) == False):
       os.mkdir(path)
    print("Saving the image " + file_name + " on directory " + path)
    
    cv2.imwrite(path +'/'+file_name, img)
    # Visualizar imagem enviada
    #cv2.imshow('URL2Image', img)
    # cv2.waitKey()

    #print("Listing directory")
    #arquivos = procurar_imagens(path)
    #for arquivo in arquivos:
    #    print('\t\t- {0}'.format(arquivo))

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),
                'size': img.size,
                'nbytes': img.nbytes,
                }
    # encode response using jsonpickle
    print("Send response: " + str(response))
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)

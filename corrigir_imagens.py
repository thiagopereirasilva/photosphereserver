# -*- coding: utf-8 -*-
"""corrigir_imagens.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10Y5l-vkqlZWloJmnOTvmuvDUT0b8SbMO

# Script feito para corrigir as imagens de renata

## Instalação das dependências
"""

!pip install piexif

"""## Definição do script

### Importação das dependências
"""

import sys, getopt, glob, piexif, os
from PIL import Image
from google.colab import files
from zipfile import ZipFile

"""### Definição de utilidade para print"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

"""### Definição da função usada para procurar as imagens"""

def procurar_imagens(pasta_fonte=''):
    """Procura as imagens em um diretório específico"""
    arquivos = glob.glob(os.path.join(pasta_fonte, '*.JPG'))

    if arquivos:
        print(bcolors.OKBLUE,
              '[Info]\t\t{0} arquivos jpg encontrados em "{1}":'.format(len(arquivos), pasta_fonte),
              bcolors.ENDC)

        for arquivo in arquivos:
            print(bcolors.OKBLUE, '\t\t- {0}'.format(arquivo), bcolors.ENDC)
    else:
        print(bcolors.WARNING,
              '[Alerta]\tNenhum arquivo JPEG encontrado em "{0}"!'.format(pasta_fonte),
              bcolors.ENDC)

    return arquivos

"""### Definição da função utilizada para alterar o parâmetro da imagem"""

def corrigir_imagens(imagens, pasta_destino=''):
    """Corrige uma lista de imagens e as salva"""
    
    for imagem in imagens:
        try:
            img = Image.open(imagem)
        except Exception:
            print(bcolors.WARNING, '[Erro]\t\tImpossível ler o arquivo "{0}"'.format(imagem), bcolors.ENDC)
            sys.exit(2)

        exif_dict = piexif.load(img.info["exif"])

        arquivo = os.path.basename(imagem)

        try:
            print(bcolors.OKBLUE, '[Info]\t\tAdicionando informação no arquivo "{0}"'.
                  format(arquivo), bcolors.ENDC)
            exif_dict['Exif'][piexif.ExifIFD.FNumber] = (71, 10)
        except Exception:
            print(bcolors.WARNING, '[Erro]\t\tErro ao tentar adicionar informação no arquivo "{0}"'.
                  format(imagem), bcolors.ENDC)
            sys.exit(2)

        exif_bytes = piexif.dump(exif_dict)
        
        if not os.path.exists(pasta_destino):
            os.mkdir(pasta_destino)
        
        nova_imagem = os.path.join(pasta_destino, arquivo)

        print(bcolors.OKBLUE, '[Info]\t\tSalvando arquivo "{0}"'.
              format(nova_imagem), bcolors.ENDC)

        img.save(nova_imagem, "jpeg", exif=exif_bytes)

"""## Usando o script

### Envio de arquivos
"""

uploaded = files.upload()

"""### Execução"""

#@title Definição dos parâmetros

nome_pasta_destino = "test" #@param {type:"string"}

imagens = procurar_imagens()
corrigir_imagens(imagens, nome_pasta_destino)

"""### Download dos arquivos"""

#@title Definição dos parâmetros

nome_pasta_origem = "test" #@param {type:"string"}
nome_aquivo_destino = "test_out" #@param {type:"string"}

imagens = procurar_imagens(nome_pasta_origem)

with ZipFile(nome_aquivo_destino,'w') as zip: 
      for imagem in imagens: 
        zip.write(imagem)

if imagens:
      files.download(nome_aquivo_destino)

from google.colab import drive
drive.mount('/content/drive')


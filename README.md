# Parte Servidor do Aplicativo PhotoSphere

Aplicativo de celular que tira 7 fotos com diferentes valores de exposição e calcula a imagem HDR resultante da combinação desta imagens.
O **front-end** da aplicação é desenvolvido em  Kotlin enquanto a parte **servidor** é desenvolvido em Python.

A parte servidor é responsável por receber e armazenar o conjunto de imagens - denominado imageset - além de gerar a imagem HDR a partir da combinação das imagens no imageset.

## Instalação, Dependências e Uso
###### Parte servidor
1 - Configurar adequadamente o arquivo de configuração config.json.
2 - Instalar o software hdrgen. É necessário a versão 32 bits da biblioteca libstdc++5:i386 (sudo apt-get install libstdc++5:i386) e a biblioteca zlib1g (sudo apt-get install zlib1g:i386)
3 - Instalar o MongoDB e criar collection (docker run -d -p 27017:27017 -p 28017:28017 mongo)
4 - Executar server.py


###### Parte Front-end
Instalar app no celular.


## Ferramentas

* [Android Studio](https://developer.android.com/studio) - Androind Studio
* [Kotlin](https://kotlinlang.org/) - Kotlin
* [Fotoapparat](https://github.com/RedApparat/Fotoapparat) - Fotoapparat API
* [camera-app](https://gabrieltanner.org/blog/camera-app) - Use case
* [Python](https://python.org) - Linguagem para criação da parte servidor
* [MongoDB](https://mongodb.org) - Banco de Dados que armazena as imagens



## Autores

* **Joao Gabrel Quaresma**
* **Thiago Silva**


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

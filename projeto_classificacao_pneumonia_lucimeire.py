# -*- coding: utf-8 -*-
"""Cópia de projeto_classificacao_pneumonia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13TH7smr8mmi_Zd2f11j6mYAxKxDgbG5k
"""

from google.colab import drive

drive.mount('/content/gdrive')

"""### Em 'local_data' deverá passar o caminho do dataset em zip"""

"!unzip '/content/gdrive/MyDrive/TRABALHO I.A._2023'

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.layers import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
import keras.utils as image
from keras.utils import load_img, img_to_array
import numpy as np
from keras.preprocessing import image

#Definição da rede neural
classificador = Sequential()

#Criando a camada de convolucao de 32 filtros, e dimensoes 3x3, altura e largura da imagem
classificador.add(Conv2D(32, (3,3), input_shape = (64, 64, 3), activation = 'relu'))

#Acelera o processamento com os dados em escala entre 0 e 1
classificador.add(BatchNormalization())

#Uma matrix de 4 pixels
classificador.add(MaxPooling2D(pool_size = (2,2)))

classificador.add(Conv2D(32, (3,3), input_shape = (64, 64, 3), activation = 'relu'))
classificador.add(BatchNormalization())
classificador.add(MaxPooling2D(pool_size = (2,2)))

# Transforma a matrix em um vetor
classificador.add(Flatten())

# Rede neural densa
classificador.add(Dense(units = 64, activation = 'relu'))
classificador.add(Dropout(0.2))

classificador.add(Dense(units = 64, activation = 'relu'))

# Zerando 20% das entradas
classificador.add(Dropout(0.2))
classificador.add(Dense(units = 64, activation = 'relu'))
classificador.add(Dropout(0.2))

# Camada de saida com classificação binaria
classificador.add(Dense(units = 1, activation = 'sigmoid'))

classificador.compile(optimizer = 'adam', loss = 'binary_crossentropy',
                      metrics = ['accuracy'])

# Gerando imagens aleatorias aproveitando os dados existentes
gerador_treinamento = ImageDataGenerator(rescale = 1./255,
                                         rotation_range = 7,
                                         horizontal_flip = True,
                                         shear_range = 0.2,
                                         height_shift_range = 0.07,
                                         zoom_range = 0.2)

"""### Em 'pasta_de_treino' e 'pasta_de_teste' deverá passar o caminho da pasta de treino e de teste da sua pasta contendo o dataset."""

gerador_teste = ImageDataGenerator(rescale = 1./255)

# Definindo a base de dados
base_treinamento = gerador_treinamento.flow_from_directory('/content/gdrive/MyDrive/TRABALHO I.A._2023/PNEUMONIA/chest_xray/train',
                                                           target_size = (64, 64),
                                                           batch_size = 32,
                                                           class_mode = 'binary')


base_teste = gerador_teste.flow_from_directory('/content/gdrive/MyDrive/TRABALHO I.A._2023/PNEUMONIA/chest_xray/test',
                                               target_size = (64, 64),
                                               batch_size = 32,
                                               class_mode = 'binary')

"""### Em defina o passo para o treino. Recomendável setar o tamanho do dataset de treino e para validation_teps o tamanho do dataset de teste"""

# Treinando a rede neural
classificador.fit_generator(base_treinamento, steps_per_epoch = (len(base_treinamento)),
                            epochs = 20, validation_data = base_teste,
                            validation_steps = (len(base_teste)))

# Carregando uma imagem para classificação
imagem_teste = load_img('/content/gdrive/MyDrive/TRABALHO I.A._2023/PNEUMONIA/chest_xray/test/NORMAL/IM-0010-0001.jpeg',
                              target_size = (64,64))

imagem_teste = img_to_array(imagem_teste)
imagem_teste /= 255
imagem_teste = np.expand_dims(imagem_teste, axis = 0)

#Realizando a previsão
previsao = classificador.predict(imagem_teste)
base_treinamento.class_indices
previsao

previsao, base_treinamento.class_indices

classificador.save('pneumonia.h5')


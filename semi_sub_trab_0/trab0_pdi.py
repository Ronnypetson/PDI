# -*- coding: utf-8 -*-

#!wget http://www.ic.unicamp.br/~helio/imagens_png/baboon.png
#!apt-get -qq install -y libsm6 libxext6 && pip install -q -U opencv-python

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

"""1.1 Histograma de imagens"""

pic_name = sys.argv[1]

im = cv2.imread(pic_name,cv2.IMREAD_GRAYSCALE)

plt.figure(1)
plt.hist(im.ravel(),256,[0,256])
plt.xlabel('Niveis de cinza')
plt.ylabel('Frequencia')
plt.savefig('hist_'+pic_name)

"""1.2 Estatísticas de imagem"""

print('largura: %d'%im.shape[1])
print('altura: %d'%im.shape[0])
print('intensidade mínima: %d'%np.min(im))
print('intensidade máxima: %d'%np.max(im))
print('intensidade média: %.2f'%np.mean(im))

"""1.3 Transformação de intensidade

*   Negativo da imagem
"""

neg = cv2.bitwise_not(im)
#plt.figure(2)
#plt.imshow(neg,cmap='gray')
cv2.imwrite('negative_'+pic_name,neg)

"""*   Converter intensidades para o intervalo [120,180]"""

im_ = np.zeros(im.shape,dtype=int)
for r in range(im_.shape[0]):
  for c in range(im_.shape[1]):
    im_[r][c] = int(60*im[r][c]/255.0) + 120

#plt.figure(3)
#plt.imshow(im_,cmap='gray',vmin=120,vmax=180)
cv2.imwrite('lin_transf_'+pic_name,im_)


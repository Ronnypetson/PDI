# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Máscaras para setar 1 e 0 em cada posição {0,...,7}
set_1 = {0:1,1:2,2:4,3:8,4:16,5:32,6:64,7:128} # aplicar bitwise OR
set_0 = {0:254,1:253,2:251,3:247,4:239,5:223,6:191,7:127} # aplicar bitwise AND

# Protótipo: 'python decodificar.py imagem_saida.png plano_bits texto_saida.txt'
in_file = sys.argv[1]
plano = int(sys.argv[2])
text_file = sys.argv[3]

# Carrega e exibe a imagem
in_img = cv2.imread(in_file)
if(len(in_img.shape) > 2):
	num_canais = in_img.shape[2]
else: # Para funcionar com imagens monocromáticas
	num_canais = 1
plt.figure(1)
plt.grid(False)
plt.title('Imagem a ter mensagem extraida')
plt.imshow(cv2.cvtColor(in_img,cv2.COLOR_BGR2RGB))

# Decodificar a mensagem da imagem
bit_pos = 0
curr_char = np.uint8(0) # caractere a ser preenchido
final_msg = ""
for i in range(in_img.shape[0]):
  for j in range(in_img.shape[1]):
    for k in range(num_canais):
      if((in_img[i][j][k]>>plano)%2 == 1): # verifica o bit escondido no plano escolhido
        curr_char |= set_1[bit_pos]
      else:
        curr_char &= set_0[bit_pos]
      bit_pos += 1
      if(bit_pos%8 == 0):
        final_msg += chr(curr_char)
        curr_char = np.uint8(0)
        bit_pos = 0

with open(text_file,'w') as out_text:
	out_text.write(final_msg) # Abrir em um editor de texto, não com 'cat'

# Visualizar os planos 0, 1, 2 e 7 de cada canal da imagem
planos = [0,1,2,7]
if(num_canais == 1):
	nomes_canais = ['Gray']
else:
	nomes_canais = ['R','G','B']
for i in range(num_canais):
  for j in range(len(planos)): # para cada plano
    plano_img = np.zeros((in_img.shape[0],in_img.shape[1]),np.uint8)
    for k in range(plano_img.shape[0]):
      for l in range(plano_img.shape[1]):
        plano_img[k][l] = 255*((in_img[k][l][i]>>planos[j])%2)
    plt.figure(num_canais*j+i+3)
    plt.grid(False)
    plt.title('Imagem do canal ' + nomes_canais[i] + ', plano ' + str(planos[j]))
    plt.imshow(plano_img,cmap='gray')
    cv2.imwrite(nomes_canais[i]+'_plano_'+str(planos[j])+'_'+in_file,plano_img)
plt.show()


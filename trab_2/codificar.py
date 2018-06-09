# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Máscaras para setar 1 e 0 em cada posição {0,...,7}
set_1 = {0:1,1:2,2:4,3:8,4:16,5:32,6:64,7:128} # aplicar bitwise OR
set_0 = {0:254,1:253,2:251,3:247,4:239,5:223,6:191,7:127} # aplicar bitwise AND

# Protótipo: 'python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png'
in_file = sys.argv[1]
text_file = sys.argv[2]
plano = int(sys.argv[3])
out_file = sys.argv[4]

# Carrega e exibe a imagem
in_img = cv2.imread(in_file)
if(len(in_img.shape) > 2):
	num_canais = in_img.shape[2]
else: # Para funcionar com imagens monocromáticas
	num_canais = 1
plt.figure(1)
plt.grid(False)
plt.title('Imagem de entrada')
plt.imshow(cv2.cvtColor(in_img,cv2.COLOR_BGR2RGB))

# Carrega a mensagem
with open(text_file,'r') as txt_fl:
  msg = txt_fl.read()

# Codifica a mensagem na imagem
byte_pos = 0 # posição do caractere atual
bit_pos = 0 # posição do bit atual
curr_char = np.uint8(ord(msg[0]))
for i in range(in_img.shape[0]):
  for j in range(in_img.shape[1]):
    for k in range(num_canais): # cada canal
      if(curr_char%2 == 1):
        in_img[i][j][k] |= set_1[plano]
      else:
        in_img[i][j][k] &= set_0[plano]
      curr_char >>= 1
      bit_pos += 1
      if(bit_pos%8==0): # Um caractere completo
        byte_pos += 1
        if(byte_pos < len(msg)):
          curr_char = np.uint8(ord(msg[byte_pos])) # Avança para o próximo caractere da mesangem
        else:
          break
    if(byte_pos >= len(msg)):
      break
  if(byte_pos >= len(msg)):
      break

# Mostra a imagem com mensagem escondida
plt.figure(2)
plt.grid(False)
plt.title('Imagem com mensagem escondida')
plt.imshow(cv2.cvtColor(in_img,cv2.COLOR_BGR2RGB))
cv2.imwrite(out_file,in_img)
plt.show()


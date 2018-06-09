# -*- coding: utf-8 -*-

import sys
import numpy as np
import scipy.stats as stat
import imutils
import cv2
from matplotlib import pyplot as plt

# Ex.: $ python alinhar.py imagem_entrada.png modo imagem_saida.png
# modo é "hough" ou "proj"
in_flname = sys.argv[1]
modo = sys.argv[2]
out_flname = sys.argv[3]

if(modo not in ['hough','proj']):
  print("O modo deve ser uma das opções:\n'proj'\tMétodo de função objetivo sobre projeção horizontal\n'hough'\tMétodo das linhas de hough")
  exit()

# Carrega imagem do caminho de entrada
in_img = cv2.imread(in_flname)
img_gray = cv2.cvtColor(in_img,cv2.COLOR_BGR2GRAY)
plt.figure()
plt.grid(False)
plt.imshow(img_gray,cmap='gray')

if modo == 'proj':
  # Método da Projeção Horizontal
  img_median = cv2.medianBlur(img_gray,5)
  _,img_bin = cv2.threshold(img_median,230,255,cv2.THRESH_BINARY)
  img_bin = cv2.bitwise_not(img_bin)
  min_ent = np.Infinity
  for a in range(-45,46,1):
    ph = np.sum(imutils.rotate_bound(img_bin,a),axis=1) # Obtém projeção horizontal
    ent = stat.entropy(ph)
    if(ent < min_ent): # Entropia mínima da projeção horizontal
      min_ent = ent
      ang = a
elif modo == 'hough':
  # Método das linhas de Hough
  img_edges = cv2.Canny(img_gray,50,150,apertureSize=3) # Aplica filtro para destacar bordas
  lines = cv2.HoughLines(img_edges,1,np.pi/180,50) # Obtém os (rho, theta) da trasformada
  ang = []
  for rho, theta in lines[0]:
    ang.append(90-theta*180/np.pi) # Seleciona o ângulo encontrado pela transformada e converte para graus
  ang = min(ang)

print('Ângulo encontrado para alinhar a imagem: %d graus'%-ang)
# imutils.rotate_bound evita que a imagem seja cortada
# O sentido do angulo do imutils.rotate_bound é o oposto do cv2.warpAffine 
img_rotated = imutils.rotate_bound(img_gray,ang)
plt.figure()
plt.grid(False)
plt.imshow(img_rotated,cmap='gray')
# Salvar a imagem rotacionada
success = cv2.imwrite(out_flname,img_rotated)
plt.show()


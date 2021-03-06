# -*- coding: utf-8 -*-

#!wget http://www.ic.unicamp.br/~helio/imagens_png/baboon.png
#!wget http://www.ic.unicamp.br/~helio/imagens_png/butterfly.png
#!wget http://www.ic.unicamp.br/~helio/imagens_png/city.png
#!wget http://www.ic.unicamp.br/~helio/imagens_png/house.png
#!wget http://www.ic.unicamp.br/~helio/imagens_png/seagull.png
#!wget https://i.ytimg.com/vi/QHqOp21jBpI/maxresdefault.jpg

import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

# Interpolação 'nearest neighbor'
def nearest(x,y,img):
  x_ = int(round(x))
  y_ = int(round(y))
  if(x_ >= 0 and x_ < img.shape[1] and y_ >= 0 and y_ < img.shape[0]):
    return img[y_][x_]
  else:
    return 0

# Interpolação bilinear
def bilinear(x,y,img): # Assume que img tem uma borda
  x_ = int(x)
  y_ = int(y)
  if(x_ >= 1 and x_ < img.shape[1]-1 and y_ >= 1 and y_ < img.shape[0]-1):
    dx = x-x_
    dy = y-y_
    return (1-dx)*(1-dy)*img[y_][x_] + dx*(1-dy)*img[y_+1][x_] \
    + (1-dx)*dy*img[y_][x_+1] + dx*dy*img[y_+1][x_+1]
  else:
    return 0

# Interpolação bicúbica
def P(t):
  return max(0.0,t)

def R(s):
  return (P(s+2)**3-4*P(s+1)**3+6*P(s)**3-4*P(s-1)**3)/6

def bicubica(x,y,img): # Assume que img tem uma borda de espessura 2
  x_ = int(x)
  y_ = int(y)
  if(x_ >= 2 and x_ < img.shape[1]-2 and y_ >= 2 and y_ < img.shape[0]-2):
    dx = x-x_
    dy = y-y_
    f_acc = 0.0
    for m in range(-1,3): # -1,0,1,2
      for n in range(-1,3):
        f_acc += img[y_+m][x_+n]*R(m-dx)*R(dy-n)
    return f_acc
  else:
    return 0

# Interpolação por polinômio de Lagrange
def L(n,dx,x_,y_,img):
  return (-dx*(dx-1)*(dx-2)*img[y_-1][x_+n-2])/6 \
  + ((dx+1)*(dx-1)*(dx-2)*img[y_][x_+n-2])/2 \
  + (-dx*(dx+1)*(dx-2)*img[y_+1][x_+n-2])/2 \
  + (dx*(dx+1)*(dx-1)*img[y_+2][x_+n-2])/6

def lagrange(x,y,img): # Assume que img tem uma borda de espessura 2
  x_ = int(x)
  y_ = int(y)
  if(x_ >= 2 and x_ < img.shape[1]-2 and y_ >= 2 and y_ < img.shape[0]-2):
    dx = x-x_
    dy = y-y_
    return (-dy*(dy-1)*(dy-2)*L(1,dx,x_,y_,img))/6 \
    + ((dy+1)*(dy-1)*(dy-2)*L(2,dx,x_,y_,img))/2 \
    + (-dy*(dy+1)*(dy-2)*L(3,dx,x_,y_,img))/2 \
    + (dy*(dy+1)*(dy-1)*L(4,dx,x_,y_,img))/6
  else:
    return 0

interps = {'nearest':nearest,'bilinear':bilinear,'bicubica':bicubica,'lagrange':lagrange}

# Argumentos de entrada
args = {}
for i in range(1,len(sys.argv)):
  if(sys.argv[i] in ['-a','-e','-d','-m','-i','-o']):
    j = 1
    args[sys.argv[i]] = []
    while(i+j < len(sys.argv) and sys.argv[i+j] not in ['-a','-e','-d','-m','-i','-o']):
      args[sys.argv[i]].append(sys.argv[i+j])
      j += 1
#print(args)

img_path = args['-i'][0] # 'img.jpg'
interpolation = args['-m'][0] # 'bilinear'
out_path = args['-o'][0] # 'result_'+img_path
option = sys.argv[1] # '-a'
img_in = cv2.imread(img_path,0)
plt.figure(1)
plt.imshow(img_in,cmap='gray')

img_height = img_in.shape[0]
img_width = img_in.shape[1]
center_x = img_width/2
center_y = img_height/2

img_in_pad1 = np.pad(img_in,(1,1),'edge') # Cria borda
img_in_pad2 = np.pad(img_in,(2,2),'edge')

if(interpolation=='bilinear'): img_in = img_in_pad1
elif(interpolation in ['bicubica','lagrange']): img_in = img_in_pad2

if(option=='-a'):
  angle = -float(args['-a'][0])*np.pi/180 # -np.pi/4
  sin_t = np.sin(-angle) # ângulo da rotação inversa
  cos_t = np.cos(-angle)
  sin_ = np.sin(angle)
  cos_ = np.cos(angle)

  # Diferença entre alturas/larguras máximas e mínimas para obter nova altura e largura depois da transformação
  vert_heights = [sin_*(j-center_x)+cos_*(i-center_y) for i in [0,img_height] for j in [0,img_width]]
  vert_widths = [cos_*(j-center_x)-sin_*(i-center_y) for i in [0,img_height] for j in [0,img_width]]
  new_height = int(max(vert_heights)-min(vert_heights))
  new_width = int(max(vert_widths)-min(vert_widths))
  new_center_x = new_width/2
  new_center_y = new_height/2

  img_out = np.zeros((new_height,new_width))

  # Rotação
  for i in range(new_height):
    for j in range(new_width):
      # Encontrar o ponto inverso de (i,j) na imagem original
      j_ = cos_t*(j-new_center_x)-sin_t*(i-new_center_y)
      i_ = sin_t*(j-new_center_x)+cos_t*(i-new_center_y)
      i_ += center_y
      j_ += center_x
      # Aplicar interpolação
      img_out[i][j] = (interps[interpolation])(j_,i_,img_in)
  plt.figure(2)
  plt.imshow(img_out,cmap='gray')
  plt.show()
  cv2.imwrite(out_path,img_out)
elif(option in ['-e','-d']):
  if(option=='-e'):
    scale_x = float(args['-e'][0]) # 0.5
    scale_y = float(args['-e'][0]) # 0.5
    new_height = int(img_height*scale_y)
    new_width = int(img_width*scale_x)
  elif(option=='-d'):
    new_height = int(args['-d'][0]) # 200
    new_width = int(args['-d'][1]) # 200
    scale_x = float(new_width)/img_width
    scale_y = float(new_height)/img_height
  new_center_y = new_height/2
  new_center_x = new_width/2

  img_scaled = np.zeros((new_height,new_width))

  # Escala
  for i in range(new_height):
    for j in range(new_width):
      # Encontrar o ponto inverso de (i,j) na imagem original
      i_ = (i-new_center_y)/scale_y
      j_ = (j-new_center_x)/scale_x
      i_ += center_y
      j_ += center_x
      # Aplicar interpolação
      img_scaled[i][j] = (interps[interpolation])(j_,i_,img_in)
  plt.figure(2)
  plt.imshow(img_scaled,cmap='gray')
  plt.show()
  cv2.imwrite(out_path,img_scaled)
else:
  print('Opção inválida. Uso:')
  print('prog \\')
  print('\t[-a ângulo] \\')
  print('\t[-e fator de escala] \\')
  print('\t[-d largura altura] \\')
  print('\t[-m interpolação] \\')
  print('\t[-i imagem] \\')
  print('\t[-o imagem] \\')


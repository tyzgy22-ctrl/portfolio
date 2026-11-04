# Текстура экрана ноутбука = фон первого экрана сайта
import numpy as np
from PIL import Image
W,H=1600,1000
y,x=np.mgrid[0:H,0:W].astype(np.float32)
base=np.array([13,15,20],np.float32)
img=np.ones((H,W,3),np.float32)*base
def glow(cx,cy,rx,ry,col,a):
    d=((x-cx)/rx)**2+((y-cy)/ry)**2
    k=np.clip(1-d,0,1)**2*a
    return k[...,None]*(np.array(col,np.float32)-base)
img+=glow(W*0.8,0,W*0.45,H*0.5,(106,168,255),0.6)
img+=glow(W*0.1,H*0.85,W*0.4,H*0.45,(124,240,180),0.42)
g=((x%80<1.2)|(y%80<1.2)).astype(np.float32)
fade=np.clip(1-(((x-W/2)/(W*0.6))**2+((y-H*0.45)/(H*0.7))**2),0,1)
img+=g[...,None]*fade[...,None]*16
Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save("screen.png")
Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save("../video/hero-bg.jpg",quality=88)
print("ok")

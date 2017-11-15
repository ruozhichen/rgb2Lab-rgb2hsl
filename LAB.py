# -*- coding: utf-8 -*-
import math 
import numpy as np
import time

def rgb2lab(inputColor):
	RGB=[0,0,0]
	for i in range(0,len(inputColor)):
		RGB[i]=inputColor[i]/255.0

	X=RGB[0]*0.4124+RGB[1]*0.3576+RGB[2]*0.1805
	Y=RGB[0]*0.2126+RGB[1]*0.7152+RGB[2]*0.0722
	Z=RGB[0]*0.0193+RGB[1]*0.1192+RGB[2]*0.9505
	XYZ=[X,Y,Z]
	XYZ[0]/=95.045/100
	XYZ[1]/=100.0/100
	XYZ[2]/=108.875/100

	L=0
	for i in range(0,3):
		v=XYZ[i]
		if v>0.008856:
			v=pow(v,1.0/3)
			if i==1:
				L=116.0*v-16.0
		else:
			v*=7.787
			v+=16.0/116
			if i==1:
				L=903.3*XYZ[i]
		XYZ[i]=v

	a=500.0*(XYZ[0]-XYZ[1])
	b=200.0*(XYZ[1]-XYZ[2])
	Lab=[int(L),int(a),int(b)]
	return Lab

# colors size: n*3, when n is very large, it improves speed using matrix calculation
def rgb2lab_matrix(colors):
	n=len(colors)
	colors=np.array(colors)
	colors=colors.astype('float')
	RGBs=colors/255.0 
	Xs=RGBs[:,0]*0.4124+RGBs[:,1]*0.3576+RGBs[:,2]*0.1805
	Ys=RGBs[:,0]*0.2126+RGBs[:,1]*0.7152+RGBs[:,2]*0.0722
	Zs=RGBs[:,0]*0.0193+RGBs[:,1]*0.1192+RGBs[:,2]*0.9505
	XYZs=np.vstack((Xs,Ys,Zs)).transpose()  
	
	XYZs[:,0]=XYZs[:,0]/(95.045/100.0)
	XYZs[:,1]=XYZs[:,1]/(100.0/100.0)
	XYZs[:,2]=XYZs[:,2]/(108.875/100.0)
	L=np.zeros((n,3),dtype='float')
	for i in range(0,3):
		v=XYZs[:,i]
		vv=np.where(v>0.008856,v**(1.0/3),v*7.787+16.0/116)
		L[:,i]=np.where(v>0.008856,116.0*vv-16.0,v*903.3)
		XYZs[:,i]=vv

	As=500.0*(XYZs[:,0]-XYZs[:,1])
	Bs=200.0*(XYZs[:,1]-XYZs[:,2])
	Ls=L[:,1]
	LABs=np.vstack((Ls,As,Bs)).transpose()
	LABs=LABs.astype('int')
	return LABs


def lab2rgb(inputColor):
	L=inputColor[0]
	a=inputColor[1]
	b=inputColor[2]
	#d=6.0/29
	T1=0.008856
	T2=0.206893
	d=T2
	fy =math.pow( (L + 16) / 116.0,3)
	fx = fy + a / 500.0
	fz = fy - b / 200.0
	#Y = fy > d ? fy * fy * fy : (fy - 16.0 / 116) * 3 * d * d
	fy = (fy) if (fy > T1) else ( L/903.3)
	Y=fy
	fy=(math.pow(fy,1.0/3)) if (fy > T1) else (7.787*fy+16.0/116)  # calculate XYZ[1], XYZ[0]=a/500.0+XYZ[1]

	# compute original XYZ[0]
	fx=fy+a/500.0
	X=(math.pow(fx,3.0)) if (fx > T2) else ((fx-16.0/116)/7.787)  # v^3>T1, so v>T1^(1/3)=

	# compute original XYZ[2]
	fz=fy-b/200.0
	Z=(math.pow(fz,3.0)) if (fz >T2) else ((fz-16.0/116)/7.787)

	X*=0.95045
	Z*=1.08875
	R = 3.240479 * X + (-1.537150) * Y + (-0.498535) * Z
	G = (-0.969256) * X + 1.875992 * Y + 0.041556 * Z
	B = 0.055648 * X + (-0.204043) * Y + 1.057311 * Z
	#R = max(min(R,1),0)
	#G = max(min(G,1),0)
	#B = max(min(B,1),0)
	RGB = [R, G, B];
	for i in range(0,3):
		RGB[i] = min(int(round(RGB[i] * 255)),255)
		RGB[i] = max(RGB[i],0)
	return RGB

# colors size: n*3, when n is very large, it improves speed using matrix calculation
def lab2rgb_matrix(colors):
	n=len(colors)
	colors=np.array(colors)
	Ls=colors[:,0]
	As=colors[:,1]
	Bs=colors[:,2]
	T1=0.008856
	T2=0.206893
	d=T2
	fys=((Ls+16)/116.0)**3.0
	fxs=fys+As/500.0
	fzs=fys-Bs/200.0
	Xs=np.zeros((n),dtype='float')
	Ys=np.zeros((n),dtype='float')
	Zs=np.zeros((n),dtype='float')

	fys=np.where(fys>T1,fys,Ls/903.3)
	Ys=fys
	fys=np.where(fys>T1,fys**(1.0/3),fys*7.787+16.0/116)

	fxs=fys+As/500.0
	Xs=np.where(fxs>T2,fxs**3.0,(fxs-16.0/116)/7.787)

	fzs=fys-Bs/200.0
	Zs=np.where(fzs>T2,fzs**3.0,(fzs-16.0/116)/7.787) 

	Xs*=0.95045
	Zs*=1.08875
	Rs = 3.240479 * Xs + (-1.537150) * Ys + (-0.498535) * Zs
	Gs = (-0.969256) * Xs + 1.875992 * Ys + 0.041556 * Zs
	Bs = 0.055648 * Xs + (-0.204043) * Ys + 1.057311 * Zs
	RGBs=np.vstack((Rs,Gs,Bs)).transpose() 
	RGBs=np.maximum(RGBs*255,0.0)
	RGBs=np.minimum(RGBs,255.0)
	RGBs=RGBs.astype('int')
	return RGBs

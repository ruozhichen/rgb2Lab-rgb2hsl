import LAB
import numpy as np
import random
import time
import HSL


n=600*900
colors=np.random.randint(0,255,size=(900*600,3))
# rgb2hsl
start1=time.time()
hsls=[]
for i in range(n):
	hsls.append(HSL.rgb2hsl(colors[i]))
end1=time.time()

# rgb2hsl_matrix
start2=time.time()
hsls=HSL.rgb2hsl_matrix(colors)
end2=time.time()

print '1',end1-start1  #4.782s
print '2',end2-start2  # 0.156s

# hsl2rgb
start3=time.time()
for i in range(n):
	HSL.hsl2rgb(hsls[i])
end3=time.time()

# hsl2rgb_matrix
start4=time.time()
rgbs=HSL.hsl2rgb_matrix(hsls)
end4=time.time()
print '3',end3-start3 #3.249s
print '4',end4-start4 #0.140s

# rgb2lab
start1=time.time()
labs=[]
for i in range(n):
	LAB.rgb2lab(colors[i])
end1=time.time()
# rgb2lab_matrix
start2=time.time()
labs=LAB.rgb2lab_matrix(colors)
end2=time.time()

print '1',end1-start1  # 5.923s
print '2',end2-start2  # 0.234

# lab2rgb
start3=time.time()
for i in range(n):
	LAB.lab2rgb(labs[i])
end3=time.time()
# lab2rgb_matrix
start4=time.time()
rgbs=LAB.lab2rgb_matrix(labs)
end4=time.time()
print '3',end3-start3 # 7.313s
print '4',end4-start4 # 0.235s
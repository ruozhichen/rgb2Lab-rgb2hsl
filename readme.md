 ## Color Space Conversion

It can convert rgb to lab, lab to rgb, rgb to hsl and hsl to rgb.

RGB：0...255

LAB：

​	L：Lightness 0...100  

​	A:  	-128...127 

​	B:	-128...127

HSL:  

​	h(float): hue 0...1 

​	s(float): Saturation 0...1  (0=toward grey, 1=pure color)

​	l(float): Lightness 0...1  (0=black 0.5=pure color 1=white)

As we often need to convert the whole image colors, I also add matrix calculation so the speed could be very fast when we need to convert a lot of colors at once.

### rgb2lab,lab2rgb

**Single color conversion**

```python
import LAB
rgb=[123,245,211]
lab=LAB.rgb2lab(rgb)
rgb=LAB.lab2rgb(lab)
```
**Multi colors conversion**

```python
import LAB
import numpy as np
colors=np.random.randint(0,255,size=(900*600,3))
labs=LAB.rgb2lab_matrix(colors)
rgbs=LAB.lab2rgb_matrix(labs)
```
### rgb2hsl,hsl2rgb

**Single color conversion**

```python
import HSL
rgb=[123,245,211]
hsl=HSL.rgb2hsl(rgb)
rgb=HSL.hsl2rgb(hsl)
```

**Multi colors conversion**

```python
import LAB
import numpy as np
colors=np.random.randint(0,255,size=(900*600,3))
hsls=LAB.rgb2hsl_matrix(colors)
rgbs=LAB.hsl2rgb_matrix(hsls)
```



**Time comparison**

For n is 600*900, the time table is as follows. We can see using matrix calculation is much faster and it saves a lot of time.

```
|   time   | single for n times | matrix |
| -------- |:------------------:|:------:|
| rgb2lab  |      5.923s        | 0.234s |
| lab2rgb  |      7.313s        | 0.235s |
|          |                    |        |
| rgb2hsl  |      4.782s        | 0.156s |
| hsl2rgb  |      3.249s        | 0.140s |
```
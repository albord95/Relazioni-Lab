from pylab import *
from gvar import gvar

hene = array([1088, 1092, 1094])
rosso = array([1065, 1054])
verde = array([1306, 1293])

s = sqrt((std(hene)**2 + std(rosso)**2 + std(verde)**2) / 3)
    
HeNe_l = array([gvar(1088, 5), gvar(1092, 5), gvar(1094, 5)])
HeNe_d = array([gvar(345,1), gvar(345,1), gvar(345,1)])

rosso_l = array([gvar(1065, 5), gvar(1054, 5)])
rosso_d = array([gvar(345,1), gvar(346,1)])

verde_l = array([gvar(1306, 5), gvar(1293, 5)])
verde_d = array([gvar(347,1), gvar(347,1)])


def d_lambda(m, d):
    l = 2*d/m*1000 #nm
    return l

def d_media_lambda(x):
    m = gvar(0,0)
    for i in range(len(x)):
        m = m + x[i]
    m = m / len(x)
    return m

l_hene = d_lambda(HeNe_l, HeNe_d)
l_rosso = d_lambda(rosso_l, rosso_d)
l_verde = d_lambda(verde_l, verde_d)

print('HeNe:  ', l_hene, '   media: ', d_media_lambda(l_hene))
print('rosso:  ', l_rosso, '   media: ', d_media_lambda(l_rosso))
print('verde:  ', l_verde, '   media: ', d_media_lambda(l_verde))




    


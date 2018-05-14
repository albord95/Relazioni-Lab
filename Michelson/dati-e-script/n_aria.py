from pylab import *
from gvar import gvar

d = gvar(50000, 50) #um

m_hene = gvar(43,1)
m_rosso = gvar(41,1)
m_verde = gvar(51,1)

l_hene = 0.6328 #um
l_rosso = 0.650 #um
l_verde = 0.532 #um

def n(m, l, d):
    return (m * l) / (2 * d) + 1

print('n_hene = ', n(m_hene,l_hene,d))
print('n_rosso =', n(m_rosso,l_rosso,d))
print('n_verde =', n(m_verde,l_verde,d))
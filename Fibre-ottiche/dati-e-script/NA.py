'script per calcolo apertura numerica di una fibra ottica'

import pylab as py
from lab import fit_curve

files = ['borcapFOLAN3.txt',
         'borcapFOMAN4.txt']

py.figure(1).set_tight_layout(True)
py.clf()
NA_prima = py.ones(len(files))
NA_dopo = py.ones(len(files))
NA_m = py.ones(len(files))

for i in range(len(files)):
    filename= files[i]
    ang, P = py.loadtxt(filename, unpack=True)
    dang = py.ones(len(ang))*0.5
    dP = P*0.03
    
    Pmax = max(P)
    P5 = Pmax*0.05 #P al 5% di P_max 
    
    #trovo l'indice corrispondente a P_max così da avere il massimo in 0
    m = 0 
    while P[m]<Pmax:
        m = m + 1
    ang = ang - ang[m]
    
    ##faccio il grafico
    py.figure(1)
    py.subplot(2,1,i+1)
    py.errorbar(ang, P, dP, dang, '.', color='tab:red', markersize='1')
    
    #prendo un po' di punti attorno al 5% di P_max               
    indici_prima = []
    indici_dopo = []
    level = 3
    
    j = 0
    while P[j]<P5:
        j = j + 1
    
    k = j-level
    while k < j+level:
        indici_prima.append(k)
        k = k + 1
        
    j = len(P)-1
    while P[j]<P5:
        j = j - 1
    
    k = j+level
    while k > j-level:
        indici_dopo.append(k) 
        k = k - 1
    
    #uso una parabola per interpolare (attenzione uso x = ay^2 + by + c)
    def parabola(y, a, b, c):
        return a*(y**2) + b*y + c
    
    out = fit_curve(parabola, P[indici_prima], ang[indici_prima],p0=[1,3.6,0], method = 'odrpack')
    par1 = out.par
    ang_prima = parabola(P5, *par1)
    out = fit_curve(parabola, P[indici_dopo], ang[indici_dopo],p0=[-1,1,0], method = 'odrpack')
    par2 = out.par
    print(par1)
    print(par2)
    ang_dopo = parabola(P5, *par2)
    ang_m = (ang_dopo-ang_prima)/2
    ang_prima = ang_prima*py.pi/180
    ang_dopo = ang_dopo*py.pi/180
    ang_m = ang_m*py.pi/180
    NA_m[i] = py.sin(ang_m)
    NA_prima[i] = py.sin(ang_prima)
    NA_dopo[i] = py.sin(ang_dopo)
    
    py.ylabel('potenza [$\mu$W]', fontsize='large')
    py.xlabel('θ [deg]', fontsize='large')
    py.plot(parabola(py.sort(P[indici_prima]), *par1), py.sort(P[indici_prima]), '-c', linewidth=2)
    py.plot(parabola(py.sort(P[indici_dopo]), *par2), py.sort(P[indici_dopo]), '-c', linewidth=2)
    
    py.plot([min(ang), max(ang)], [P5, P5], '-', linewidth=1, color='tab:green')
    


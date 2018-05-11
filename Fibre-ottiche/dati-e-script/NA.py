'script per calcolo apertura numerica di una fibra ottica'

import pylab as py
from lab import fit_curve

files = ['borcapFOLAN3.txt',
         'borcapFOMAN4.txt']

py.figure(1).set_tight_layout(True)
py.clf()

for i in range(len(files)):
    filename= files[i]
    ang, P = py.loadtxt(filename, unpack=True)
    dang = py.ones(len(ang))*0.5
    dP = P*0.03
    
    ##faccio il grafico
    py.figure(1)
    py.subplot(2,1,i+1)
    py.errorbar(ang, P, dP, dang, '.', markersize='1')
    
    P5 = max(P)*0.05 #P al 5% di P_max
    level = 7 
    
    #prendo un po' di punti attorno al 5% di P_max               
    indici_prima = []
    indici_dopo = []
    zona = 'prima'
    
    for k in range(len(P)):
        if P[k] < max(P):
            zona = 'prima'
        else:
            zona = 'dopo'
        if (zona == 'prima') & (P[k] > P5 - level) & (P[k] < P5 + level):
            indici_prima.append(k)
        if (zona == 'dopo') & (P[k] > P5 - level) & (P[k] < P5 + level):
            indici_dopo.append(k)
            
    if min(len(indici_prima), len(indici_dopo)) < 10:
        print('ATTENZIONE: pochi punti per interpolare')
    
    
    #uso una parabola per interpolare (attenzione uso x = ay^2 + by + c)
    def parabola(y, a, b, c):
        return a*(y**2) + b*y + c
    
    out = fit_curve(parabola, P[indici_prima], ang[indici_prima], p0=[1,1,1], absolute_sigma=False)
    par1 = out.par
    ang_prima = parabola(P5, *par1)
    out = fit_curve(parabola, P[indici_dopo], ang[indici_dopo], p0=[1,1,1], absolute_sigma=False)
    par2 = out.par
    ang_dopo = parabola(P5, *par2)
    NA_prima = py.sin(ang_prima)
    NA_dopo = py.sin(ang_dopo)
    
    py.ylabel('potenza [$\mu$W]', fontsize='large')
    py.xlabel('θ [deg]', fontsize='large')
    py.plot(parabola(py.sort(P[indici_prima]), *par1), py.sort(P[indici_prima]), '-c', linewidth=2)
    py.plot(parabola(py.sort(P[indici_dopo]), *par2), py.sort(P[indici_dopo]), '-c', linewidth=2)
    
    #py.plot([ang_prima, ang_dopo], [HM, HM], '-', linewidth=2, color='tab:red', label='{} = {}°'.format(ang_p[i], round(FWHM,1)))
    #py.legend(fontsize='large')
    


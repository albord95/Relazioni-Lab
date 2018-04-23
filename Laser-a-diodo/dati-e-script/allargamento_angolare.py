'''script che calcola l'allargamento angolare del diodo laser'''

import pylab as py
from lab import fit_curve, xe

files = ['borcapLDVangPER.txt',
         'borcapLDVangPAR.txt']

py.figure(1).set_tight_layout(True)
py.clf()
ang_p = ['$angolo_{\perp}$', '$angolo_{//}$']

for i in range(len(files)):
    filename= files[i]
    ang, I = py.loadtxt(filename, unpack=True)
    dang = py.ones(len(ang))*0.5
    dI = py.ones(len(I))*0.01
    
    ##faccio il grafico
    py.figure(1)
    py.subplot(2,1,i+1)
    py.errorbar(ang, I, dI, dang, '.', markersize='1')
    
    altezza = max(I) - min(I)
    level = altezza/3
    HM = (min(I) + max(I)) / 2 #I a metà altezza
        
    #prendo un po' di punti attorno alla metà altezza               
    indici_prima = []
    indici_dopo = []
    zona = 'prima'
    
    for k in range(len(I)):
        if ang[k] < 0:
            zona = 'prima'
        else:
            zona = 'dopo'
        if (zona == 'prima') & (I[k] > HM - level) & (I[k] < HM + level):
            indici_prima.append(k)
        if (zona == 'dopo') & (I[k] > HM - level) & (I[k] < HM + level):
            indici_dopo.append(k)
            
    if min(len(indici_prima), len(indici_dopo)) < 10:
        print('ATTENZIONE: pochi punti per interpolare')
    
    
    
    def parabola(y, a, b, c):
        return a*(y**2) + b*y + c
    #uso una parabola per interpolare (attenzione uso x = ay^2 + by + c)
    out = fit_curve(parabola, I[indici_prima], ang[indici_prima], p0=[1,1,1], absolute_sigma=False)
    par1 = out.par
    ang_prima = parabola(HM, *par1)
    out = fit_curve(parabola, I[indici_dopo], ang[indici_dopo], p0=[1,1,1], absolute_sigma=False)
    par2 = out.par
    ang_dopo = parabola(HM, *par2)
    FWHM = ang_dopo - ang_prima
    
    ylabel('segnale [$\mu$A]', fontsize='large')
    xlabel('{} [°]'.format(ang_p[i]), fontsize='large')
    py.plot(parabola(sort(I[indici_prima]), *par1), sort(I[indici_prima]), '-c', linewidth=2)
    py.plot(parabola(sort(I[indici_dopo]), *par2), sort(I[indici_dopo]), '-c', linewidth=2)
    
    py.plot([ang_prima, ang_dopo], [HM, HM], '-', linewidth=2, color='tab:red', label='{} = {}°'.format(ang_p[i], round(FWHM,1)))
    legend(fontsize='large')
    
    print('FWHM = ', FWHM)
    
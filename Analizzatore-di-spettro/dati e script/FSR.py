"""script sottoinsieme di modi_laser_HeNe.py che calcola la FSR"""

from pylab import *
from scipy.optimize import curve_fit
from lab import fit_curve, xe
from gvar import gvar

files = ['borcapasv02.txt',
         'borcapasv03.txt',
         'borcapasv04.txt',
         'borcapasv05.txt',
         'borcapasv06.txt',
         'borcapasv07.txt',
         'borcapasv10.txt',
         'borcapasv11.txt',
         'borcapasv12.txt',
         'borcapasv13.txt',
         'borcapasv14.txt',
         'borcapasv15.txt',
         'borcapasv16.txt']

altezza = 3
larghezza = 5

##funzioncina che cerca gli indici dei massimi di un vettore
def massimi(array):
    """Se i massimi sono il primo e l'ultimo elemento non li prende.
       Se ci sono piĂš valori uguali prende l'indice del primo."""
    massimi = []
    for i in range(1, len(array)-1):
        if (array[i-1] < array[i]) & (array[i] >= array[i+1]):
            massimi.append(i)
    return massimi

numero_ordini = []
##funzione di fit
def retta(x, a, b):
    return a*x + b

FSRs = []
dFSRs = []
for i in range(len(files)):
    filename= files[i]    
    t, volt, _, __, rampa, ___ = loadtxt(filename, comments='"', unpack=True)
    t = t*1000 #millisecondi
    volt = volt*1000 #millivolt
    rampa = rampa*1000 #millivolt
    
    ##cerco i minimi
    minimi = massimi(-volt)
    
    voltmean = volt.mean()
    voltstd = volt.std()
    triggerlevel = voltmean - 0.5*voltstd
    
    ##prendo solo i minimi sotto il triggerlevel (e dentro la rampa)
    maxindex = argmax(rampa)
    minindex = argmin(rampa)
    picchi = []
    for j in range(len(minimi)):
        if (min(minindex, maxindex) < minimi[j]) & (minimi[j] < max(minindex, maxindex)+3):
            if (volt[minimi[j]] < triggerlevel):
                picchi.append(minimi[j]) 
    
    ##tolgo i picchi di ordini incompleti 
    ##(solo il primo e l'ultimo ordine possono essere incompleti)
    diffpicchi = diff(picchi)
    meandiffpicchi = diffpicchi.mean()
    if diffpicchi[0] > meandiffpicchi:
        picchi = picchi[1:]
    elif diffpicchi[1] > meandiffpicchi:
        picchi = picchi[2:]
    if diffpicchi[-1] > meandiffpicchi:
        picchi = picchi[:-1]
    elif diffpicchi[-2] > meandiffpicchi:
        picchi = picchi[:-2]
        
    ##trovo i deltanu con un fit    
    figure('FSR')
    subplot(altezza, larghezza, i+1)
    n_ordini = int(len(picchi)/3)
    numero_ordini.append(n_ordini)
    ordini = linspace(1, n_ordini, n_ordini)
    ordini_fit = ordini - (n_ordini+1)/2
    """con questo trucco fitto una retta simmetrica rispetto all'asse y per
    avere un miglior q e per non doverne propagare l'errore"""
    m = []
    dm = []
    q = []
    dq = []
    nomipicchi = ['sinistra', 'centro  ', 'destra  ']
    for k in range(3):
        piccoinquestione = picchi[k::3]
        plot(ordini, t[piccoinquestione], 'o', color='tab:red', markersize='4')
        """come errore metto (1/2)*sensibilità*0.68,
        scelta discutibile ma giustificata a spanne dal confidence level"""
        out = fit_curve(retta, ordini_fit, t[piccoinquestione], dy=0.5*0.68*(t[1]-t[0]), p0=[1,1], absolute_sigma=True)
        par = out.par
        cov = out.cov
        m_fit = par[0]
        q_fit = par[1]
        dm_fit, dq_fit = sqrt(diag(cov))
        #print('picco %s: m = %s  q = %s' %(nomipicchi[k], xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
        m.append(m_fit)
        q.append(q_fit)
        dm.append(dm_fit)
        dq.append(dq_fit)
        plot(ordini, retta(ordini_fit, *par), linewidth=1)
    m = array(m)
    dm = array(dm)
    FSR = gvar(m.mean(), dm.mean()/sqrt(3))
    FSRs.append(m.mean())
    dFSRs.append(dm.mean()/sqrt(3))
    print('FSR = ', FSR)
    figure('errori')
    errorbar(i, m.mean(), yerr=dm.mean()/sqrt(3))

FSRs = array(FSRs)
dFSRs = array(dFSRs)
print(FSRs.mean(), '+-', std(FSRs, ddof=1)/sqrt(len(FSRs)))
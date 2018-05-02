'''fit lineare per calcolo corrente di soglia del diodo laser'''

import pylab as py
from lab import fit_curve, xe

files = ['borcapLDG12PvsI.txt',
         'borcapLDG25PvsI.txt',
         'borcapLDG43PvsI.txt']

py.figure(1).set_tight_layout(True)
py.clf()

##[I]=mA e [P]=muA

T = [12, 25, 43]

for i in range(len(files)):
    filename= files[i]
    I, P = py.loadtxt(filename, unpack=True)
    dI = py.ones(len(I))*0.1
    dP = py.ones(len(P))
    for k in range(len(P)):
        dP[k] = (5*P[k])/100
    
    
    ##faccio il grafico P-I
    py.figure(1)
    py.errorbar(I, P, dP, dI, '.', markersize='3')
    
    ##estraggo i dati da fittare
    j=0
    while P[j]>300:
        j=j+1
            
    ##funzione di fit
    def retta(x, a, b):
        return a*x + b
    
    ##trovo I_th con un fit    
    m = []
    dm = []
    q = []
    dq = []
    out = fit_curve(retta, I[0:j-1], P[0:j-1], dy = dP[0:j-1], p0=[1,1], absolute_sigma=True)
    par = out.par
    cov = out.cov
    m_fit = par[0]
    q_fit = par[1]
    dm_fit, dq_fit = py.sqrt(py.diag(cov))
    I_th = -q_fit/m_fit
    dI = I_th*(dm_fit/m_fit + dq_fit/q_fit)
    print('m = %s  q = %s' %(xe(m_fit, dm_fit), xe(q_fit, dq_fit)))
    print('I_th = %s' %(xe(I_th, dI)))
    m.append(m_fit)
    q.append(q_fit)
    dm.append(dm_fit)
    dq.append(dq_fit)
    x = py.linspace(I[j]-2, I[0]+1, 100)
    py.plot(x, retta(x, *par), linewidth=1, label='{} = {} mA, T = {} °C'.format('$I_{th}$', xe(I_th, dI), T[i]))
    py.legend(fontsize='large')
    py.ylabel('P [$\mu$W]')
    py.xlabel('I [mA]')


        